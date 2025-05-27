import re 

def regex_find_all_words(self, document : str) -> list[str]:
    """
    Separates words from puncts.
    
    Args: 
        document (str): the document.
        
    Returns: 
        document_as_list (list[str]): the document as a list 
    
    """ 
    
    return re.findall(r"\b\w+\b", document)
