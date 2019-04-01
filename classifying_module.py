###
###  Descrption:  Contains the image processing of PFAS and AI classification of processed digits
###  Input:  scanned in PFAS
###  Output:  json of classified answers as strings
###

from PIL import Image
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
import pylab as pl
import numpy as np
import random
from sklearn import ensemble


def main():
    # load scanned_PFAS image

    # load premade classifier

    # crop digits (Barrett) and generate an image_dictionary with following structure:
    #     <question 1>: [ <digit 5 image>, <digit 4 image>, ... , <digit 0 image> ]
    #     <question 2>: [ <digit 5 image>, <digit 4 image>, ... , <digit 0 image> ]
    #     ...

    # iterate through all digits in image_dictionary, creating a new classified_dictionary with the following structure:
    #     <question 1>: "<six digit string>"
    #     <question 2>: "<six digit string>"
    #     ...

    # output classified dictionary to json file

main():
