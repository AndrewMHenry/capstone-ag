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


def main():
    while 1:
        # Search for file
        aiInput = "scannedPFAS"
        aiResults = "aiOut.json"
        key = "answer_key.json"
        graded = "graded.json"
        os.system("./scanning-module.sh")
        if os.path.exists(aiInput) == True:
            os.system("python3 classify_PFAS.py " + aiInput + " " + aiResults)
            move_file(aiInput)
        if os.path.exists(aiResults) == True:
            os.system("python3 new_grading.py --results " + aiResults + " --answerkey " + key + " --output " + graded)
            move_file(aiResults)
#        if os.path.exists(graded) == True:
#            os.system("python3 agtextui.py " + graded)
#            move_file(graded)

if __name__ == '__main__':
    main()
