import sys

from plagiarism_checker.plagiarism_system import Plagiarism_System


def main(): 
    
    if len(sys.argv) < 2: 
        sys.exit("please enter a filename for a document to check")
    input_file = sys.argv[1]
    system = Plagiarism_System(input_file, "docs/")
    system.compare()


if __name__ == "__main__": 
    main() 