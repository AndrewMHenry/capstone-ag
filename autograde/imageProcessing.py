# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:12:37 2019

@author: kcarr
"""

from PIL import Image
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
import pylab as pl
import numpy as np
import random
from sklearn import ensemble
#from autograde.results import write_results
#from autograde.results import read_results
from statistics import mean
import time
import pprint
pp = pprint.PrettyPrinter(depth=5)

FILENAME = 'Image_00004.bmp'

def processPFAS(FILENAME):
    #
    # load scanned_PFAS image
    #
    PFAS_image = Image.open(FILENAME).convert("L");
    PFAS_dict = {}
    
    #
    # Set coordinates
    #
    x1 = 800
    y1 = 0
    x2 = 3000
    y2 = 490
    #
    # get StudentID
    #
    PFAS_dict["StudentID"] = PFAS_image.crop( (x1, y1, x2, y2) )
    pl.matshow(PFAS_dict["StudentID"])

    #
    # Set coordinates
    #
    x1 = 590
    y1 = 505
    x2 = 3000
    y2 = 395
    yOffset = 300
    #
    # take answer strips out of the sheet & build dictionary
    #
    PFAS_dict["questions"] = {}
    for i in range(1,11):
        PFAS_dict["questions"][str(i)] = PFAS_image.crop( (x1, y1, x2, y1+yOffset-10) );
        y1 = y1 + yOffset + 12.5
        pl.matshow(PFAS_dict["questions"][str(i)])
    
    #
    # return dictionary
    #
    
    return PFAS_dict
    
processPFAS(FILENAME)
