class Doc_chunk: 
    
    def __init__(self, id : str, content : str): 
        self.id = id
        self.content = content
        self.vector = [] 
        
        
    
    def get_id(self): 
        return self.id 
    
    def get_vector(self): 
        return self.vector 
        
        
        