# Workflow

- main validates input
- main crates a system object
- main calls on system object to pre process the corpus
- preprocess will involve 
        - getting the word count of all words 
        - splitting the docs into chunks, keeping track of them with an id generated from the file name, and input or db and so on. possibly index for chunk #
        - creating a vocab array over all unique words. 
        - figuring out a way to map the words into an index, ensuring that the same index in vocab will always be for the same word. 

after prepreprocess 

create TF-IDF for all docs 

run cosine similarity for all input docs compared to all docs of the corpus. (itertool combine.pairs or whatever.)

check similarity over thresshold (> 0.8?) 

print out a report where all cases of high similarity. example: 

inp_doc-23 corpus-doc-1-29 sim 87 % 

or generalized 

inp_doc[part number] corpus-doc[identifier for main file][chunk number] sim [percentage]


classes: 

System 

    keeps track of the docs, calls preprocess to set up, calls on methods for cos sim 


Chunk 

     wraper for the document, contains an identifier and a text chunk. 



output will be printed to console, and those that are far advanced in wisdom can get that into a document by ending the cli command with >output-file.txt. 

GUIs are for those who toil for Windows, a most inferior OS. Linux is life. May thy kernel be blessed. 