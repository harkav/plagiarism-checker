import re 

def regex_find_all_words(document : str) -> list[str]:
    """
    Separates words from puncts.
    
    Args: 
        document (str): the document.
        
    Returns: 
        document_as_list (list[str]): the document as a list 
    
    """ 
    
    return [word.lower() for word in re.findall(r"\b\w+\b", document)]
