from PIL import Image
import pylab as pl
import numpy as np
import matplotlib as plt
plt.rcParams.update({'figure.max_open_warning': 0})

def load_img(img):
    imgarr = np.array(img) 
    imgarr = np.invert(img) #invert black and white for AI training data
    #pl.gray() 
    pl.matshow(imgarr) #uncomment to display
    return imgarr

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
    #print (top, bottom, x1, x2)
    img = img.crop((x1,top,x2,bottom))
    
    
    #image1 = Image.open(destPath).convert("L")   
    cropped = img.resize((8,8), resample=5)
    load_img(cropped)
    cropped.save(sourcePath, 'png')
import argparse
import collections

# --------------------------------------------------------------------------------------------------------------
def processPage():
    boxCtr = 0
    rowCtr = 1
    digitCtr = 1
    topLeftx = 282
    topLefty = 202

# --
    imageName = ("PFAS_demo_sample-1.PNG")
    imageFile = Image.open(imageName).convert("L")
    imageFile = imageFile.resize((1700,2200), resample=4)
    while (boxCtr != 264):
        if (boxCtr == 133):
            topLefty = 202
        boxCtr += 1

        if (digitCtr == 6):
            digitCtr = 0
            rowCtr += 1

        if (boxCtr > 1) and (boxCtr % 6 != 1):
            digitCtr += 1
            topLeftx += 80             # 80px to the right is the next box
        elif (boxCtr > 1) and (boxCtr % 6 == 1):
            digitCtr += 1
            if (boxCtr < 133):
                topLeftx = 282
            if (boxCtr >= 133):
                topLeftx = 982
            topLefty = topLefty + 81.5   # 81px downward is the next row

        box = (topLeftx, topLefty, topLeftx + 75, topLefty + 76)
        boxImg = imageFile.crop(box)
        # Fix the numbering/naming scheme
        boxImgName = "processedPFAS/" + str(rowCtr) + "/" + str(rowCtr) + "_" + str(digitCtr) + ".PNG"
        boxImg = boxImg.resize((32,32), resample=4)
        boxImg.save(boxImgName, "PNG")
        close_up(boxImgName)
        

def main():
    Image.MAX_IMAGE_PIXELS = None
    processPage()

main()
