import sys
import pathlib
import numpy as np
from regex_find_all_words import regex_find_all_words

"""
Project for creating vectors out of a set of document

"""


def build_word_list_from_input_and_corpus(dir_path: str, input_doc : str) -> list[str]: 
    """
    """
    
    dirpath = pathlib.Path(dir_path)
    
    all_words = set()
    
    for maybe_file in dirpath.iterdir():
        if pathlib.Path.is_file(maybe_file): 
            get_unique_words_in_a_doc(all_words, maybe_file)
    try: 
        input_path = pathlib.Path(input_doc)
        get_unique_words_in_a_doc(all_words, input_path)
    except (FileNotFoundError, IOError): 
        sys.exit("Could not read input doc")
    
    return list(sorted(all_words))

def get_unique_words_in_a_doc(all_words: set[str], maybe_file: pathlib.Path):
    """
    Extracts all unique words from a document. Mutates the set of all words in corpus + input.
    
    Args: 
        all_words (set[str]): all words found thus far.
        maybe_file (pathlib.Path): A path.
    
    
    
    """
    
    file_as_str = get_content_as_string(maybe_file)
    tokens = regex_find_all_words(file_as_str)
    tokens_lower = {token.lower() for token in tokens} # is this a proper set comprehension? 
    all_words.update(tokens_lower)
            
            
            
def get_content_as_string(filename : pathlib.Path) -> str: 

    
    with open(filename, "r") as f: 
        file_as_str = f.read()
        #print(file_as_str) works here. 
        return file_as_str
         
        
print(build_word_list_from_input_and_corpus("./test-docs", "test-input.txt"))



def create_tf_idf(vocab : list[str], doc1: str, doc2: str) -> None: 
    
    doc1_vector = np.zeros(len(vocab))
    doc2_vector = np.zeros(len(vocab))
    
    for i in vocab:
        tf_idf(term= vocab[i], doc1, all_docs)
        
    pass 
    
    


"""
ChatGpt suggested workflow for a plagiarism finder: 

Input: List of documents.

Preprocess: Tokenize and normalize each document.

Build vocabulary: Gather all unique words across corpus.

Vectorize: For each document, compute TF-IDF vector based on the vocabulary.

Compare: Compute cosine similarity between every pair of document vectors.

Detect: Flag pairs with similarity over a chosen threshold.

Output: Present flagged pairs and similarity scores.


What counts as a document? Several options, try to go for a gliding window. 

"""