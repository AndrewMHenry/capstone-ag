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
from autograde.results import write_results
from autograde.results import read_results
from statistics import mean
import time
import pprint
pp = pprint.PrettyPrinter(depth=5)


def main():
    #
    # load scanned_PFAS image
    #
    PFAS = Image.open('PFAS_demo_sample.PNG').convert("L");
    
    #
    # load premade classifier from training data
    # using the python supplied images for now
    #
    n_samples = len(trDigits.images)
    X_digits = trDigits.data #/ trDigits.data.max()
    y_digits = trDigits.target
    classifier = ensemble.RandomForestClassifier()
    classifier.fit(X_digits, y_digits)
    
    #
    # crop digits (Barrett) and generate an image_dictionary with following structure:
    #     <question 1>: [ <digit 5 image>, <digit 4 image>, ... , <digit 0 image> ]
    #     <question 2>: [ <digit 5 image>, <digit 4 image>, ... , <digit 0 image> ]
    #     ...
    #
    answerImg = {}; #answer dictionary
    answerArr = {};
    xOffset = 280;
    yOffset = 200;
    xSize = 480;
    ySize = 81.5;
    boxWidth = 81.5;
    for i in range(0, 22): #30 questions on the right
        answerArr[i] = {}
        #print ("x1: ", (xOffset), "y1: ", (xOffset + xSize) )
        #print ("x2: ", (yOffset), "y2: ", (yOffset + i*ySize) )
        x1 = xOffset; #left edge of box
        x2 = xOffset + xSize; #right edge of box
        y1 = yOffset + i*ySize + 2; #top edge of box
        y2 = yOffset + (i+1)*ySize - 3; #bottom edge of box
        answerImg[i] = PFAS.crop( (x1, y1, x2, y2) );
        answerImg[i] = answerImg[i].resize((192,32), resample=4)
        imgarr = np.array(answerImg[i])
        imgarr = np.invert(answerImg[i])
        #pl.matshow(imgarr)
        for j in range(0, 6): #6 digits
            #print ( "x1 = ", x1 + 5*boxWidth, "y1 = ", y1, "x2 = ", x1 + (5+1)*boxWidth, "y2 = ", y2) 
            tempImg = answerImg[i].crop( (j*32 + 1, 0, (j+1)*32 -1, 32 ) );
            #tempImg = PFAS.crop( (x1 + 5*boxWidth, y1,  x1 + (5+1)*boxWidth,  y2) )
            tempImg = tempImg.resize((32,32), resample=2)
            tempImg = close_up(tempImg) 
            if (tempImg is not None):    
                imgarr1 = np.array(tempImg)
                imgarr1 = np.invert(tempImg)
                print (i,j)
                #pl.matshow(imgarr1)
                answerArr[i][j] = imgarr1; 
    pp.pprint(answerArr)

    #
    # iterate through all digits in image_dictionary, creating a new classified_dictionary with the following structure:
    #     <question 1>: "<six digit string>"
    #     <question 2>: "<six digit string>"
    #     ...
    #
    # output classified dictionary to json file
    #
    outObj = {}
    outObj["name"] = str(time.time())
    outObj["questions"] = {}
    for i in range(21):
        outObj["questions"][str(i+1)] = {}
        outObj["questions"][str(i+1)]["answer"] = "";
        #pl.matshow(trDigits.images[i])
        #pl.matshow(arr[i])
        minProb = 1;
        classification = {i: [''] for i in range(6)}
        for j in range(6):
            if ( j  in answerArr[i] ):
                #print (j)
                classification[j] = classifier.predict(answerArr[i][j].reshape(1, -1))
                prob = classifier.predict_proba(answerArr[i][j].reshape(1, -1))
                minProb = min(prob[0][classification[j][0]], minProb)

        outObj["questions"][str(i+1)]["min_conf"] = minProb ;
    write_results("saved-jsons/aiOut.json", outObj)
    outObj["questions"][str(i+1)]["answer"] =  ''.join( str(classification[key][0]) for key in range(6))
    print(outObj)
    
def close_up(img):
#    img = Image.open(sourcePath)
    pixels = img.load()
    #print (img.size)
    #print (pixels[0,0])
    end = 0
    
    ####get top
    for i in range(0,31):
        for j in range(0,31):
            if (pixels[j,i] != 255):
                end = 1
        if (end == 1):
            break
    top = i - 1
    end = 0
    a=31;
    
    ####get bottom
    for a in range(31, 0, -1):
        for b in range(0, 31):
            if (pixels[b,a] != 255):
                end = 1
        if (end == 1):
            break
    
    bottom = a + 1   
    
    ####get left
    for i in range(1,31):
        for j in range(1,31):
            if (pixels[i,j] != 255):
                end = 1
        if (end == 1):
            break
    left = i
    
    ####get right
    for a in range(31, 0, -1):
        for b in range(0, 31):
            if (pixels[a,b] != 255):
                end = 1
        if (end == 1):
            break
    right = a + 1
    
    if (end == 0):
        return None
    
    height = bottom - top
    x1 = (32/2) - (height/2) #from middle x, back to make a square
    x2 = (32/2) + (height/2) #from middle x, forward to make a square
    #print (top, bottom, x1, x2)
    img = img.crop((x1,top,x2,bottom))
    
    
    #image1 = Image.open(destPath).convert("L")   
    cropped = img.resize((8,8), resample=5)
    return cropped
#    load_img(cropped)
#    cropped.save(sourcePath, 'PNG')

main()
