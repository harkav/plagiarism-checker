from multiprocessing import Pool
import pathlib
from typing import Any, NamedTuple
from plagiarism_checker.utils.cosine_similarity import cosine_similarity
from plagiarism_checker.utils.document_chuncker import (
    yield_chunk,
    build_chunk_from_text,
)
from plagiarism_checker.utils.file_to_str import (
    build_word_list_from_input_and_corpus,
    get_content_as_string,
)
from plagiarism_checker.utils.regex_find_all_words import regex_find_all_words
from itertools import product
from plagiarism_checker.doc_chunk import DocChunk
import math
import numpy as np
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class NamedProductItem(NamedTuple):
    a: Any
    b: Any
    
class CosineSimOutput(NamedTuple):
    result: float
    a_id: str
    b_id: str 


class Plagiarism_System:
    def __init__(self, input_file: str, document_dir: str):
        with tracer.start_as_current_span("init") as span:
            span.set_attribute("input_file", input_file)
            self._input_file = input_file
            self._document_dir = document_dir
            self._vocab = []  # will contain all the unique terms
            self._doc_frequency_dict = dict()
            self._mapping = None
            self._mapping_reversed = None
            # mapping.... Or mappings.
            self._doc_chunks_input = []  # might be a good idea to keep these separate.
            self._doc_chunks = []
            self.preprocess_documents(self._input_file, self._document_dir)
            self.build_vectors()

    def build_vocab(self) -> None:
        """
        Builds the vocab-arr.
        """

        self._vocab = build_word_list_from_input_and_corpus(
            self._document_dir, self._input_file
        )

    def get_paths_from_dir(self, dir: str) -> list[tuple[pathlib.Path, str]]:
        paths = []
        directory = pathlib.Path(dir)
        for file in directory.iterdir():
            if file.is_file():
                paths.append((file, file.name))
        return paths

    def preprocess_documents(self, input_file, document_dir):
        with tracer.start_as_current_span("preprocess_documents") as span:
            # preprocess the docs, fill out the constructor.
            # 1
            self.build_vocab()

            # 2

            # for input file

            input_file_as_str = get_content_as_string(self._input_file)

            for chunk_tuple in yield_chunk(input_file_as_str):
                self._doc_chunks_input.append(
                    build_chunk_from_text(chunk_tuple, doc_identifier="input")
                )

            # for corpus in db:

            for path in self.get_paths_from_dir(self._document_dir):
                corpus_file_as_str = get_content_as_string(path[0])

                for chunk_tuple in yield_chunk(corpus_file_as_str):
                    self._doc_chunks.append(
                        build_chunk_from_text(chunk_tuple, doc_identifier=path[1])
                    )

            # 3 - create mapping

            self._mapping = {i: term for i, term in enumerate(self._vocab)}
            self._mapping_reversed = {v: k for k, v in self._mapping.items()}

            # 4

            self.build_df_dict()

    def build_vectors(self) -> None:
        with tracer.start_as_current_span("build_vectors") as span:
            for chunk in self._doc_chunks_input + self._doc_chunks:
                tokens = regex_find_all_words(chunk.get_content())
                nparr = np.zeros(len(self._vocab))

                for token in tokens:
                    token = token.lower()
                    if token not in self._mapping_reversed:
                        print(token in self._vocab)
                    index = self._mapping_reversed[token]
                    nparr[index] = self.tf_idf(token, chunk)
                chunk.set_vector(nparr)

    def build_df_dict(self) -> None:
        with tracer.start_as_current_span("build_df_dict") as span:
            for term in self._vocab:
                for chunk in self._doc_chunks_input + self._doc_chunks:
                    if term.lower() in chunk.get_content():
                        self._doc_frequency_dict[term.lower()] = (
                            self._doc_frequency_dict.get(term, 0) + 1
                        )


    def compare(self):

        with tracer.start_as_current_span("compare") as span:
            # run cos sim
            p = list(map(lambda x: NamedProductItem(x[0], x[1]), product(self._doc_chunks_input, self._doc_chunks)))
            THRESHOLD = 0.85
            
            with Pool() as pool: 
                results = list(pool.map(self.find_cosine_sim_from_p, p))
                for input in sorted(results, key=lambda x: int(x.a_id.split("-")[1])):
                    if (input[0] > THRESHOLD):
                        print(f"Similarity between input doc-id {input.a_id} and {input.b_id} is {input.result * 100:.2f} %")

    def find_cosine_sim_from_p(self, input: NamedProductItem) -> CosineSimOutput:

        result = cosine_similarity(input.a.get_vector(), input.b.get_vector())

        return CosineSimOutput(result, input[0].get_id(), input[1].get_id())
            

    # consider Numba, multiprocessing.

    # Move tf-idf files into this class, since we're probably going to modify it slightly. Perhaps modify, move to ./utils/tf-idf along with cosine sim.

    def term_frequency(self, term: str, document: str) -> int:
        """
        Find term frequency in a document.

        Args:
            term (str): the term in question.
            document (str): the document, represented as a str.

        Returns:
            frequency (int): the count of term in document.

        """
        words_in_doc = [
            word.lower() for word in regex_find_all_words(document.get_content())
        ]
        count = 0

        for word in words_in_doc:
            if word == term.lower():
                count += 1
        return count

    def document_frequency(self, term: str) -> int:
        if term in self._doc_frequency_dict:
            return self._doc_frequency_dict[term]
        else:
            print(f"could not find {term}")
            return 1

    # TODO maybe consider doing with the doc frequency during the creation of the chuncks.

    def inverse_document_frequency(self, term: str) -> float:
        """
        Finds the inverse document frequency of the term.

        Args:
            term (str): the term.
            documents (list[str]): the documents.

        Returns:
            The inverse document frequency of the term.


        """

        N = len(self._doc_chunks_input + self._doc_chunks)
        df = self.document_frequency(term)

        return math.log(N / (1 + df))

    def tf_idf(self, term: str, single_document) -> float:
        #
        """
        Returns term frequency * inverse document frequency.

        Args:
            term (str): the term you're trying to find the tf-idf for.
            single_document (str): the document you're trying to find the tf-idf for.
            documents (list[str]): the whole corpus.

        Returns:
            tf-idf (float): the tf-idf based on the input.
        """
        return self.term_frequency(
            term, single_document
        ) * self.inverse_document_frequency(term)
