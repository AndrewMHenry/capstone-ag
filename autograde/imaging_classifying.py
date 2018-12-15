# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 11:29:25 2018

@author: kcarr
"""

from PIL import Image
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
import pylab as pl
import numpy as np
import random
from sklearn import ensemble
from results import write_results

trDigits = load_digits()

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


def loadPFAS():
    #find calibration (only for physically scanned PFAS)
    
    #load inage
    PFAS = Image.open('samples/PFAS_demo_sample.PNG').convert("L")
    answerImg = {}; #answer dictionary
    answerArr = {};
    xOffset = 280;
    yOffset = 200;
    xSize = 480;
    ySize = 81.5;
    boxWidth = 81.5;
    #coords: (x1, y1, x2, y2)
    for i in range(0, 22): #30 questions on the right
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
                #pl.matshow(imgarr1)
                answerArr[i] = imgarr1; 
    return answerArr
    #crop each answer box
    
    #crop each digit
    
    #zoom to fit each digit
    
#def trainClassifier():
    #properly format training data (maybe load a JSON to save on image processing time costs)
    #train classifier with data
    

def main():
    arr = loadPFAS()
    n_samples = len(trDigits.images)
    X_digits = trDigits.data / trDigits.data.max()
    y_digits = trDigits.target
    classifier = ensemble.RandomForestClassifier()
    classifier.fit(X_digits, y_digits)
    count = 0;
    outObj = {}
    outObj["name"] = "Test Student"
    outObj["questions"] = {}
    for i in range(10):
        outObj["questions"][str(i+1)] = {}
        outObj["questions"][str(i+1)]["class"] = "";
        outObj["questions"][str(i+1)]["probabilities"] = {}
        pl.matshow(trDigits.images[i])
        pl.matshow(arr[i])
        classification = classifier.predict(arr[i].reshape(1, -1))
        prob = classifier.predict_proba(arr[i].reshape(1, -1))#, (classification == i)
        outObj["questions"][str(i+1)]["class"] =  str(classification[0])
        probDict = {};
        for j in range(0,10):
            probDict[str(j)] = prob[0][j]
            #print (probDict)
        outObj["questions"][str(i+1)]["probabilities"] = [probDict];
        
        print( classification, prob )
        if (classification == i):
            count = count +1;
    write_results("saved-jsons/aiOut.json", outObj)
    print ("accuracy: ", count/10)
main()
