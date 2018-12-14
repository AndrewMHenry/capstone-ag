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
    for name in resultsDict['questions']:
        resultsDict['questions'][name]['score'] = int(resultsDict['questions'][name]['class'] == answerkeyDict[name])
    write_results('graded', resultsDict)




        

