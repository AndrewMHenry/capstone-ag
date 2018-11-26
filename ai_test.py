# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from PIL import Image
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
import pylab as pl
import numpy as np
import random
from sklearn import ensemble

trDigits = load_digits()

#crops sample data to an 8-bit image and saves it. Used for cropping indv. digits from answer
#coords: (x1, y1, x2, y2)
def cropper(sourcePath, coords, destPath):
    image1 = Image.open(sourcePath).convert("L")
    cropped = image1.crop(coords)
    cropped = cropped.resize((32,32), resample=4) #narrow scope of search 
    #save image before pixelating
    cropped.save(destPath, 'PNG')
    
    close_up(destPath) #clear excess space that would confuse ai
    
    

#crops such that the top and bottom rows have pixels
def close_up(sourcePath):
    img = Image.open(sourcePath)
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
    
    height = bottom - top
    x1 = (32/2) - (height/2) #from middle x, back to make a square
    x2 = (32/2) + (height/2) #from middle x, forward to make a square
    print (top, bottom, x1, x2)
    img = img.crop((x1,top,x2,bottom))
    
    
    #image1 = Image.open(destPath).convert("L")   
    cropped = img.resize((8,8), resample=5)
    load_img(cropped)
    cropped.save(sourcePath, 'PNG')

#loads an image for processing by the AI
def load_img(img):
    imgarr = np.array(img) 
    imgarr = np.invert(img) #invert black and white for AI training data
    #pl.gray() 
    pl.matshow(imgarr) #uncomment to display
    return imgarr
    
#Load preliminary data
def load_prelim_data():
    w = 50
    h = 50
    
    for i in range(5, 6):
        x = 2
        y = 2
        sourceName = 'samples/s' + str(i) + '.png'
        for j in range(0,9+1):
            #if (j == 7):
            #    cropper(sourceName, (x, y, x + w - 1, y + h), str(j) + '/s' + str(i) + '_' + str(j) + '.png')    
            #else:
            
            cropper(sourceName, (x, y, x + w, y + h), str(j) + '/s' + str(i) + '_' + str(j) + '.png')    
            x = x + w + 1 #next number space, plus the pixel border

def load_classifier():
    trImages = trDigits.images.reshape(len(trDigits.images), -1)
    trTargets = trDigits.targets
    classifier = ensemble.GradientBoostingClassifier()
    calssifier.fit(trImages, trTargets)
    
def main():
    load_prelim_data();
    im = []
    arr = []
    digits09 = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    for i in range(10):
        im.append( Image.open( str(i) + '/s5_' + str(i) + '.png').convert("L") )
        arr.append( load_img(im[i]) )
#    print ("OUR   width:" + str(len(arr)) + "\theight: " + str(len(arr[0])) )
#    print ("THEIR width:" + str(len(trDigits.images[0])) + "\theight: " + str(len(trDigits.images[0][0])))
#    
#    pl.gray()
#    pl.matshow(arr)
#    print(arr)
#    
#    pl.gray()
#    pl.matshow(trDigits.images[0])
#    print(trDigits.images[0])
        
    n_samples = len(trDigits.images)
    X_digits = trDigits.data / trDigits.data.max()
    y_digits = trDigits.target
    X_train = X_digits[:int(.9 * n_samples)]
    y_train = y_digits[:int(.9 * n_samples)]
    X_test = X_digits[int(.9 * n_samples):]
    y_test = y_digits[int(.9 * n_samples):]
    classifier = ensemble.RandomForestClassifier()
    classifier.fit(X_digits, y_digits)
    print ()
    #for i in range(10):
        #print(trDigits.data[i])
    for i in range(10):
        pl.matshow(trDigits.images[i])
        print( classifier.predict(arr[i].reshape(1, -1)) )
#       print(arr[i].reshape(1, -1))
main()
    