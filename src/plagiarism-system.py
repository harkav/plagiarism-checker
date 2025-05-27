from utils.cosine_similarity import cosine_similarity
from utils.document_chuncker import yield_chunk
from utils.vector_builder import build_word_list_from_input_and_corpus, get_content_as_string
from itertools import product
from doc_chunk import Doc_chunk
import math
import re 


class Plagiarism_System: 
    
    def __init__(self, input_file : str, document_dir : str): 
        self._input_file = input_file
        self._document_dir = document_dir
        self._vocab = [] # will contain all the unique terms
        self._doc_frequency_dict = dict()
        # mapping.... Or mappings.
        self._doc_chunks_input = [] # might be a good idea to keep these separate. 
        self._doc_chunks = []
        self.preprocess_documents(self, self._input_file, self._document_dir)
        
        
        
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
    
        self._vocab = build_word_list_from_input_and_corpus(self._input_file, self._document_dir)
        
        # 2 
        
        # for input file
        
        input_file_as_str = get_content_as_string(self._input_file)
        
        self._doc_chunks_input = yield_chunk(input_file_as_str)
        
        
            

    
    
    def build_df_dict(self): 
        
        for term in self._vocab: 
            
            for doc in zip(self._doc_chunks_input, self._doc_chunks): 
                if term in doc: 
                    if self._doc_frequency_dict[term]: 
                        self._doc_frequency_dict[term] +=1 
                    else: 
                        self._doc_frequency_dict[term] = 1
    
    
    
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
        words_in_doc = [word.lower() for word in self.regex_find_all_words(document)]
        count = 0
        
        for word in words_in_doc: 
            if word == term.lower():
                count += 1
        return count
        
        
        


    def document_frequency(self) -> int: 
      
       
        return self._doc_frequency_dict["term"]

    #TODO maybe consider doing with the doc frequency during the creation of the chuncks. 


    def inverse_document_frequency(self, term: str, documents: list[str]) -> float: 
        """
        Finds the inverse document frequency of the term.
        
        Args: 
            term (str): the term.
            documents (list[str]): the documents.
            
        Returns:
            The inverse document frequency of the term.

        
        """
        
        N = len(documents)
        df = self.document_frequency(term, documents)
        
        
        return math.log(N / (1 + df))


    def tf_idf(self, term: str, single_document: list[str], documents: list[str]) -> float: 
        
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
        return self.term_frequency(term, single_document) * self.inverse_document_frequency(term, documents)


