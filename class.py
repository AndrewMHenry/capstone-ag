import os
from os import walk
from PIL import Image


def cropper(sourcePath, coords, destPath):
    image1 = Image.open(sourcePath).convert("L")
    cropped = image1.crop(coords)
    cropped = cropped.resize((32,32), resample=4) #narrow scope of search 
    #save image before pixelating
    cropped.save(destPath, 'PNG')
    
    close_up(destPath)

arr=[]
dir = "/Users/yvonne3/envs/capstone-ag/capstone-ag/data-samples/gathered_data"
for (dirpath, dirnames, filenames) in walk(dir):
	for file in filenames:
		filepath = os.path.join(dirpath, file)
		f = open(filepath, "rb")  #remove b
		arr.append(f.read())
		f.close()

print("################# PRINTING ARRAY ##################")
print (arr)

