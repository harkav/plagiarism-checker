from plagiarism_checker.utils.length_normalization import length_normalization
from plagiarism_checker.utils.dotproduct import dot_product

def cosine_similarity(vector1: list[float], vector2 : list[float]) -> float :
    """
    A method for finding the cosine similarity of two vectors.
    
    Args: 
        vector1 (list[float]): a list representing a vector.
        vector2 (list[float]): a list representing a different vector. 
        
    Returns: 
        dotproduct (float): the dot product of the normalized vectors.
        
    Raises: 
        ValueError: If the vectors are not of the same length. 
    """
    
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be of the same length")
        
    
    vector1_normalized = length_normalization(vector1)
    vector2_normalized = length_normalization(vector2)
    
    return dot_product(vector1_normalized, vector2_normalized)
