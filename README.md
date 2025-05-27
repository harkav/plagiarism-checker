# Plagiarism checker 

This is a program meant to check an input document for plagiarism compared to a set of other documents.
I would not, however, recommend taking it too seriously, since the possiblity of both false positives and 
false negatives are quite real. 

The project started out when I tried to implement a few algorithms for NLP in Python. I asked chatgpt 
for a few suggestions for what you could do with just these algorithms, and one of the things that it 
suggested was a plagiarism checker. 

It was a great way to dig down into the algorithms and to understand how they actually work. 
It used to be quite hard for me to understand how natural language can be represented in a meaningful 
way, and that is much clearer now. I guess then, that the main goal of this project is to learn more 
about NLP, and not so much about actually checking a document for plagiarism. 


# How to install. 

Download the files, from root, 

```bash 
pip install -e .

```

# How to run

```bash 
plagiarism-checker [input_file]

example: 

plagiarism-checker ./test_input/test-input.txt


```
you can also add > output.txt after the final argument to get the output in a file rather than in the terminal. 


# Usage of LLMs, citations. 

These algorithms were taught in a course I did at UiO some time ago, though the Python implementation is my own. 
There are several libraries that offer the same algorithm, and they are probably much more performant, but I wanted 
to implement them myself from the ground up. 

It was chatgpt that introduced the idea, but with two exceptions, the code is my own. So is the structure and the main flow 
of the program, all though I have used chatgpt for troubleshooting bugs, sanity checks and someone to 
bounce ideas off of when I've stuggled to deal with the cognitive complexity of the show. 
I did use chatgpt quite exstensibly for getting the import statements and the structure of the files right. 
Almost all of the .toml file is written by chatgpt. 

The following are written by chatgpt in the main code: 
 the regex expression: 
an elegant short hand for dict insertions: (self._doc_frequency_dict[term.lower()] = self._doc_frequency_dict.get(term, 0) + 1))


This book was used during the course that I took, and while it is dense, I think it can be a great way to get 
into NLP. It also covers most of the algorithms that I've used. 

https://web.stanford.edu/~jurafsky/slp3/

All of the text docs are things that I've written over the years and published here and there. None of it should be copy-righter though. 

# TO-DOs 

More clean up, using doc strings all over the place, more comments. Thinking about some optimizations, primarily whether there is a way to avoid vectorizing the reference corpus every time the program runs. 