
I've used a bit of chatgpt for this task. 

With two exceptions, all code in ./src is written directly by me, but the entirty of the launch.json file is written by chatgpt. 
The exceptions are the regex expression and a short-hand for dict en tries (self._doc_frequency_dict[term.lower()] = self._doc_frequency_dict.get(term, 0) + 1)

I was implementing a few algorithms used in NLP in python for vector similarity and prompted chatgpt for an idea for anything fun I could do with these algorithms, and chatgpt suggested a plagiarism checker. We discussed the idea on a high level, but the pipeline and structure of the program was designed, and implemented by me. 

Chatgpt has helped me with the debugging and sanity checks, as well as helping me walk through the program conceptiually when the cognitive complexity has been 
a bit much for my meager mortal mind. 

When I've used chatgpt for this project, I have tried to prompt it in such a way that it will answer in a more general way, i.e. not provide code or a complete answer, but rather help me think. 

It might help me with creating a toml file to make it easier to run, haven't thought about that yet. 

The text docs (in /docs and the testinputs) are based on things I've written in the past. 

