from typing import Generator
from plagiarism_checker.utils.regex_find_all_words import regex_find_all_words

"""

Program for chunking a document

"""



def yield_chunk(document: str): 
    
    document_as_list = regex_find_all_words(document)
    SLIDING_WINDOW = 25
    CHUNK_SIZE = 50
    MAX_INDEX = len(document_as_list) - CHUNK_SIZE
    index = 0
    
    while index < MAX_INDEX: 
        chunk = " ".join(document_as_list[index: index + CHUNK_SIZE])
        yield chunk
        index += SLIDING_WINDOW
    # the tail end of the document will be ignored. Can review at some point. 
        
        
    
    