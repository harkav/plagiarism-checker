from plagiarism_checker.utils.length_normalization import length_normalization
from plagiarism_checker.utils.dotproduct import dot_product
from opentelemetry import trace
from opentelemetry.trace import NoOpTracerProvider
tracer = trace.get_tracer(__name__, tracer_provider=NoOpTracerProvider())

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
    with tracer.start_as_current_span("cosine_similarity") as span:
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")

        span.set_attribute("vector_1_len", len(vector1))
        span.set_attribute("vector_2_len", len(vector2))
        vector1_normalized = length_normalization(vector1)
        span.add_event("normalized vector 1")
        vector2_normalized = length_normalization(vector2)
        span.add_event("normalized vector 2")
        return dot_product(vector1_normalized, vector2_normalized)
