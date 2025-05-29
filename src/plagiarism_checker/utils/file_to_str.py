import sys
import pathlib
from plagiarism_checker.utils.regex_find_all_words import regex_find_all_words

"""
Module for buildin a list of all words in reference files and input file
"""


def build_word_list_from_input_and_corpus(dir_path: str, input_doc: str) -> list[str]:
    """
    Builds the vocab list.

    Args:
        dir_path (str): the path to the reference docs as a str.
        input_doc (str): the path to the input file as a str.

    Returns:
        result (list[str]): a sorted list of all the words in the vocab.
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

    return [word.lower() for word in list(sorted(all_words))]


def get_unique_words_in_a_doc(all_words: set[str], maybe_file: pathlib.Path) -> None:
    """
    Extracts all unique words from a document. Mutates the set of all words in corpus + input.

    Args:
        all_words (set[str]): all words found thus far.
        maybe_file (pathlib.Path): A path.


    """

    file_as_str = get_content_as_string(maybe_file)
    tokens = regex_find_all_words(file_as_str)
    tokens_lower = {
        token.lower() for token in tokens
    }  # is this a proper set comprehension?
    all_words.update(tokens_lower)


def get_content_as_string(filename: pathlib.Path) -> str:
    """
    Extracts the content of a file and returns it as a str.
    
    Args: 
        filename (pathlib.Path): the filename as a str.
        
    Returns: 
        file_as_str (str): the content of a text file.        
    """
    with open(filename, "r") as f:
        file_as_str = f.read()
        # print(file_as_str) works here.
        return file_as_str


#TODO: this assumes a readable text file, doesn't it? Maybe add some tests. 