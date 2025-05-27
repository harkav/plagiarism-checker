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


test_string = """
for så å gå videre fra slike ting som en
frakk, en hund, en hest, til et landområde, til deg selv, til
kroppen din og dens enkelte deler, til dine barn, kona di,
brødrene dine. Se deg rundt i alle retninger og kast disse
tingene fra deg. Rens vurderingene dine slik at du ikke er
knyttet til noe som ikke er ditt eget, eller blir en del av
deg, eller at det forårsaker deg smerte når det blir revet
fra deg. Og si til deg selv når du trener deg selv slik hver
dag, slik du gjør på skolen, ikke at du er en ﬁlosof, (for du
må gå med på at dette er en pretensiøs tittel), men at du
er en slave som er i ferd med å bli frigjort, for dette er den
sanne friheten. Og det var på denne måten at Diogenes
ble satt fri av Antisthenes17, og dette han mente da han
sa at han ikke lenger kunne gjøres til en slave av noen.

"""

print(regex_find_all_words(test_string))

print(len(test_string.split()) == len(regex_find_all_words(test_string)))



with open("test-regex-doc.txt", "r") as f: 
    test_string2 = f.read()
    
print(regex_find_all_words(test_string2))

print(len(regex_find_all_words(test_string)) == len(regex_find_all_words(test_string2)))