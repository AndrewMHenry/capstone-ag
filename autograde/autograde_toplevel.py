import glob
import os
import os.path
import shutil
import sys

SAVED_RESULTS_DIR = 'saved-results'

def move_file(filename):
    """Move file to subdirectory of saved results."""
    moved_filename = os.path.join(SAVED_RESULTS_DIR, filename)

    if os.path.exists(moved_filename):
        os.remove(moved_filename)

    shutil.move(filename, moved_filename)


def file_exists(filename):
    return os.path.isfile(QUIT_FILE)


QUIT_FILE = 'quit'


def main():
    while not file_exists(QUIT_FILE):
        # Search for file
        aiInput = "scannedPFAS"
        aiResults = "aiOut.json"
        key = "answer_key.json"
        graded = "graded.json"
        os.system("./scanning-module.sh")
        if os.path.exists(aiInput) == True:
            os.system("./our_python classify_PFAS.py " + aiInput + " " + aiResults)
            move_file(aiInput)
        if os.path.exists(aiResults) == True:
            os.system("./our_python new_grading.py --results " + aiResults + " --answerkey " + key + " --output " + graded)
            move_file(aiResults)
#        if os.path.exists(graded) == True:
#            os.system("python3 agtextui.py " + graded)
#            move_file(graded)

if __name__ == '__main__':
    main()
