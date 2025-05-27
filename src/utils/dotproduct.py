
def dot_product(vector1: list[float], vector2 : list[float]) -> float :
    """
    A method for finding the dot product of two vectors.
    
    Args: 
        vector1 (list[float]): a list representing a vector.
        vector2 (list[float]): a list representing a different vector. 
        
    Returns: 
        sum (float): the sum of the calculation.
        
    Raises: 
        ValueError: If the vectors are not of the same length. 
    """
    
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be of the same length")
    if len(vector1) == 0: 
        return 0
        
    
    total = 0 
    for v1, v2 in zip(vector1, vector2): 
        total += (v1 * v2)
    return total

