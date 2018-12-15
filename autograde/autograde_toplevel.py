import glob
import os
import os.path
import sys

def main():
    while 1:
        # Search for file
        aiResults = "aiOut.json"
        key = "ai-answer-key.txt"
        graded = "graded"
        if os.path.exists(aiResults) == True:
            os.system("python3 grading.py --results " + aiResults + " --answerkey " + key)
        if os.path.exists(graded) == True:
            os.system("python3 agtextui.py " + graded)

if __name__ == '__main__':
    main()
