import glob
import os
import os.path

def main():
    while 1:
        # Search for file
        aiResults = "results.txt"
        key = "answerkey.txt"
        if os.path.exists(aiResults) == True:
            os.system("python3 autograde/grading.py --results " + aiResults + " --answerkey " + key)
            graded = "graded.txt"
            os.system("python3 autograde/agtextui.py --graded" + graded)

if __name__ == '__main__':
    main()
