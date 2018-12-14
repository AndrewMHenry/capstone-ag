#from PIL import Image
import matplotlib.pyplot as plt
import argparse
import sys
import numpy as np
import random
from autograde.results import read_results, write_results
#from sklearn import ensemble

def main():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--results")
    parser.add_argument("--answerkey")

    args = parser.parse_args()

    # Read in
    resultsDict = read_results(args.results)
    answerkeyDict = read_results(args.answerkey)
    
    # compare answers between AI results and answer key
    # totalPoints = 0
    for name in resultsDict['questions']:
    #    totalPoints += 1
        answer = answerkeyDict[name]
        studentAnswer = resultsDict['questions'][name]['class']
        resultsDict['questions'][name]['score'] = int(studentAnswer == answer)
        # go into probabilities dict, pull out probability each digit is right, and multiply them together
        resultsDict['questions'][name]['correctConf'] = resultsDict['questions'][name]['probabilities'][0][answer]
        resultsDict['questions'][name]['evalConf'] = resultsDict['questions'][name]['probabilities'][0][studentAnswer]
    write_results('graded', resultsDict)




        

