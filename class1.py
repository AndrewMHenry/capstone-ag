import os
from os import walk
from PIL import Image
import matplotlib.pyplot as plt
#from sklearn.datasets import load_digits
import pylab as pl
import numpy as np

#from sklearn import ensemble

def cropper(sourcePath, coords, destPath):
    image1 = Image.open(sourcePath).convert("L")
    cropped = image1.crop(coords)
    cropped = cropped.resize((32,32), resample=4) #narrow scope of search 
    #save image before pixelating
    cropped.save(destPath, 'PNG')
    data = np.asarray(cropped).reshape(-1)
    return data
    close_up(destPath)


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

def load_img(img):
    imgarr = np.array(img)
    imgarr = np.invert(img) #invert black and white for AI training data        
    #pl.gray()                                                                  
    pl.matshow(imgarr) #uncomment to display                                    
    return imgarr



# think of this part as main. since python doesnt care. be a visionary!
arr=[]
dir = "/Users/yvonne3/envs/capstone-ag/capstone-ag/data-samples/gathered_data"
j = 0
arr2 =[]
#for (dirpath, dirnames, filenames) in walk(dir):
#    for file in filenames:
#                j+=1
#                if file == ".DS_Store":
#                    continue
#                filepath = os.path.join(dirpath, file)
#                cropper(filepath, (2, 2, 52, 52), "cropped/"+str(j)+'.PNG')
#                print("Cropped " + file) #prints image name to screen
#                arr.append("cropped/"+str(j)+'.PNG') #puts cropped images into array
                #f = open(filepath, "rb")  #remove b if you don't want to read in bytes                      
                #arr.append(f.read())                                                                        
                #f.close()

for i in range(10):
    dirname = os.path.join(dir, str(i))
    for filename in os.listdir(dirname):
        actual_filename = os.path.join(dirname, filename)
        j+=1
        if actual_filename == ".DS_Store":
            continue

        data = cropper(actual_filename, (2, 2, 52, 52), "cropped/"+str(j)+'.PNG') 
        print("Cropped " + actual_filename) #prints image name to screen                                 
        arr2.append(i)
        #here we append the data returned from cropper function
        arr.append(data) #puts cropped images into array
        

        
print(arr) 

x = np.array(arr)
y = np.array(arr2)


np.save('array', x)
np.save('array2' , y)
#from cropper, extract numbers
#from cropper, return data as numpyarray
                                                                                       
#create array of the same size of the previous one: arr2.append(i)

#convert into numpyarrays (arr and arr2. by using import numpy as np, np.arr)
#save numpyarray into file: arr.save. 
