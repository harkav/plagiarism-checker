import pathlib
import sys
from plagiarism_checker.utils.cosine_similarity import cosine_similarity
from plagiarism_checker.utils.document_chuncker import yield_chunk, build_chunk_from_text
from plagiarism_checker.utils.vector_builder import build_word_list_from_input_and_corpus, get_content_as_string
from plagiarism_checker.utils.regex_find_all_words import regex_find_all_words
from itertools import product
from plagiarism_checker.doc_chunk import Doc_chunk
import math
import numpy as np


class Plagiarism_System: 
    
    def __init__(self, input_file : str, document_dir : str): 
        self._input_file = input_file
        self._document_dir = document_dir
        self._vocab = [] # will contain all the unique terms
        self._doc_frequency_dict = dict()
        self._mapping = None
        self._mapping_reversed = None
        # mapping.... Or mappings.
        self._doc_chunks_input = [] # might be a good idea to keep these separate. 
        self._doc_chunks = []
        self.preprocess_documents(self._input_file, self._document_dir)
        self.build_vectors()
        
        
        
    
    def build_vocab(self) -> None: 
        self._vocab = build_word_list_from_input_and_corpus(self._document_dir, self._input_file)
        
        
    def get_paths_from_dir(self, dir : str) -> list[tuple[pathlib.Path, str]]: 
        
        paths = []
        directory = pathlib.Path(dir)
        for file in directory.iterdir(): 
            if file.is_file(): 
                paths.append((file, file.name))
        return paths  
    
    def preprocess_documents(self, input_file, document_dir): 
         
    # preprocess the docs, fill out the constructor. 
    
        """
        Sketched workflow, might not be the right order
        
        1 build vocab from docs
        
        2 build chunks from docs 
        
        3 build a mapping from an index to the vocablist
        
        4 build dfs
        
        vector creation can be separated out to a different function, already getting long
        
        compare will deal with the comparisons 
        
        
        
        """
        
        # 1 
        self.build_vocab()
        
        # 2 
        
        # for input file
        
        input_file_as_str = get_content_as_string(self._input_file)
        
        for chunk_tuple in  yield_chunk(input_file_as_str): 
            self._doc_chunks_input.append(build_chunk_from_text(chunk_tuple, doc_identifier="input"))
        
        
        # for corpus in db: 
        
        for path in self.get_paths_from_dir(self._document_dir): 
            corpus_file_as_str = get_content_as_string(path[0])
            
            for chunk_tuple in yield_chunk(corpus_file_as_str): 
                self._doc_chunks.append(build_chunk_from_text(chunk_tuple, doc_identifier=path[1]))
            
        
            
        # 3 - create mapping
        
        self._mapping = {i : term for i, term in enumerate(self._vocab)}
        self._mapping_reversed = {v : k for k, v in self._mapping.items()}
        
        
        #4 
        
        self.build_df_dict()
    
    
    def build_vectors(self)-> None: 
        
        
        for chunk in self._doc_chunks_input + self._doc_chunks: 
            tokens = regex_find_all_words(chunk.get_content())
            nparr = np.zeros(len(self._vocab))
            
            for token in tokens: 
                token = token.lower()
                if token not in self._mapping_reversed: 
                    continue
                index = self._mapping_reversed[token]
                nparr[index] = self.tf_idf(token, chunk)
            chunk.set_vector(nparr)
                
            
    
    
    def build_df_dict(self) -> None: 
        
        for term in self._vocab: 
            for chunk in self._doc_chunks_input + self._doc_chunks: 
                if term in chunk.get_content(): 
                    self._doc_frequency_dict[term] = self._doc_frequency_dict.get(term, 0) + 1
    
    
    
    def compare(self): 
        # run cos sim
        THRESHOLD = 0.8
        
        for input_chunk, db_chunk in product(self._doc_chunks_input, self._doc_chunks): 
            # chatgpt told me about itertools.product
    
            result = cosine_similarity(input_chunk.get_vector(), db_chunk.get_vector())
            if result > THRESHOLD: 
                result = result * 100
                print(f"Similarity between input doc-id {input_chunk.get_id()} and {db_chunk.get_id()} is {result:.2f} %")    
    
    

# consider Numba, multiprocessing. 

# Move tf-idf files into this class, since we're probably going to modify it slightly. Perhaps modify, move to ./utils/tf-idf along with cosine sim. 

  


    def term_frequency(self, term : str, document: str) -> int:
        """
        Find term frequency in a document. 
        
        Args: 
            term (str): the term in question.
            document (str): the document, represented as a str.
            
        Returns:
            frequency (int): the count of term in document.

        """ 
        words_in_doc = [word.lower() for word in regex_find_all_words(document.get_content())]
        count = 0
        
        for word in words_in_doc: 
            if word == term.lower():
                count += 1
        return count
        
        
        


    def document_frequency(self, term : str) -> int: 
      
       
        return self._doc_frequency_dict[term]

    #TODO maybe consider doing with the doc frequency during the creation of the chuncks. 


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
        return self.term_frequency(term, single_document) * self.inverse_document_frequency(term)


