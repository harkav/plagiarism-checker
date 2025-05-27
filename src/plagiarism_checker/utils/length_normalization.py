import math

def length_normalization(vector: list[float]) -> list[float] :
    """
    A method for normalizing a vector.
    
    Args: 
        vector1 (list[float]): a list representing a vector.
         
        
    Returns: 
        normalized_vector (list[float]): the sum of the calculation.
        
    Raises: 
        ValueError: If it is a zero-length vector. 
    """
    
 
    
    total = 0
    for element in vector: 
        total += element ** 2
    length = math.sqrt(total)
    
    if length == 0: 
        raise ValueError("cannot normalize a zero-length vector")
    normalized_vector = [x/ length for x in vector]

    return normalized_vector


