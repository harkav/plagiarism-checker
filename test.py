

arr = ["kvakk", "kvekk", "kvokk"]

mapping = {i: term for i, term in enumerate(arr)}

print(mapping)


def reverse_dict(dictoinary): 
    
    new_dict = {}
    
    for k, v in dictoinary.items(): 
        new_dict[v] = k
    return new_dict