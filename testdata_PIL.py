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
    cropped.save(sourcePath, 'PNG')

# --------------------------------------------------------------------------------------------------------------
def processPage():
    boxCtr = 0
    digitCtr = -1

    # Coordinates of the top left corner of the first (hand-written) box
    # Possibly starting at second row.
    topLeftx = 204
    topLefty = 431
    chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    charCtr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pageCtr = 1

    # 96 (hand-written) boxes on each page; started counting at 1 not 0
    while (pageCtr != 17):
        if (boxCtr == 96):
            boxCtr = 0
            digitCtr = -1
            pageCtr += 1
            topLeftx = 204
            topLefty = 431

# --
        imageName = ("data-samples/PNGs/agscan1200_0000-" + str(pageCtr) + ".PNG")
        imageFile = Image.open(imageName).convert("L")

        while (boxCtr != 96):
            boxCtr += 1
            digitCtr += 1

            if (digitCtr == 12):
                digitCtr = 0

            if (boxCtr > 1) and (boxCtr % 12 != 1):
                topLeftx += 109             # 109px to the right is the next box
            elif (boxCtr > 1) and (boxCtr % 12 == 1):
                topLeftx = 207
                topLefty = topLefty + 196   # 196px downward is the next row

# originally +105
            box = (topLeftx, topLefty, topLeftx + 86, topLefty + 86)
            boxImg = imageFile.crop(box)
            boxImgName = "data-samples/gathered_data/" + chars[digitCtr] + "/s" + chars[digitCtr] + "_" + str(charCtr[digitCtr]) + ".PNG"
            boxImg = boxImg.resize((32,32), resample=4)
            boxImg.save(boxImgName, "PNG")
            close_up(boxImgName) 
          
            charCtr[digitCtr] += 1

def main():
    Image.MAX_IMAGE_PIXELS = None
    processPage()

main()