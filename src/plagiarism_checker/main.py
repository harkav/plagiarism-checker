import os
print("PYTHONPATH:", os.getenv("PYTHONPATH"))


from plagiarism_checker.plagiarism_system import Plagiarism_System


def main(): 
    system = Plagiarism_System("testinput3.txt", "docs/")
    print(len(system._vocab))
    #print(system._vocab[600:700])
    print("diogenes" in system._vocab)
    print("Diogenes" in system._vocab)
    system.compare()


if __name__ == "__main__": 
    main() 