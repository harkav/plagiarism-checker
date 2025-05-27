

from plagiarism_checker.plagiarism_system import Plagiarism_System


def main(): 
    system = Plagiarism_System("testinput3.txt", "docs/")
    system.compare()


if __name__ == "__main__": 
    main() 