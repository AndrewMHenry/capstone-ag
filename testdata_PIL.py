from PIL import Image

# --------------------------------------------------------------------------------------------------------------
def processPage():
    boxCtr = 0
    digitCtr = -1

    # Coordinates of the top left corner of the first (hand-written) box
    topLeftx = 204
    topLefty = 431
    chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    charCtr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pageCtr = 1

    # 96 (hand-written) boxes on each page; started counting at 1 not 0
    while (pageCtr != 17):
        if (boxCtr == 97):
            boxCtr = 0
            digitCtr = -1
            pageCtr += 1
            topLeftx = 204
            topLefty = 431

        charCtr[digitCtr] += 1
# --
        imageName = ("data-samples/PNGs/agscan1200_0000-" + str(pageCtr) + ".PNG")
        imageFile = Image.open(imageName)

        while (boxCtr != 97):
            boxCtr += 1
            digitCtr += 1

            if (digitCtr == 12):
                digitCtr = -1

            if (boxCtr > 1) and (boxCtr % 13 != 0):
                topLeftx += 109             # 109px to the right is the next box
            elif (boxCtr % 13 == 0):
                topLeftx = 204
                topLefty = topLefty + 196   # 196px downward is the next row

            box = (topLeftx, topLefty, topLeftx + 105, topLefty + 105)
            boxImg = imageFile.crop(box)
            boxImgName = "data-samples/gathered_data/" + chars[digitCtr] + "/s" + chars[digitCtr] + "_" + str(charCtr[digitCtr]) + ".PNG"
          #  boxImg.resize((32,32), resample=4)
            boxImg.save(boxImgName, "PNG")

def main():
    Image.MAX_IMAGE_PIXELS = None
    processPage()

main()