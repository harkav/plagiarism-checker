from typing import Generator
from tf_idf import pre_process

"""

Program for chunking a document

"""



def yield_chunk(document: str) -> Generator[str]: 
    
    document_as_list = pre_process(document)
    SLIDING_WINDOW = 25
    CHUNK_SIZE = 50
    MAX_INDEX = len(document_as_list) - CHUNK_SIZE
    index = 0
    
    while index < MAX_INDEX: 
        chunk = " ".join(document_as_list[index: index + CHUNK_SIZE])
        yield chunk
        index += SLIDING_WINDOW
    # the tail end of the document will be ignored. Can review at some point. 
        
        
    
    
with open("test-doc-2.txt", "r") as f: 
    doc = f.read()
    
    for i in yield_chunk(doc): 
        print(i)
        print("\n")