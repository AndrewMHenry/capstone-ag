
"""
Adapted from

http://hanzratech.in/2015/02/24/handwritten-digit-recognition-using-opencv-sklearn-and-python.html

"""



# Import the modules
import argparse
import collections
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np

import matplotlib.pyplot as plt

import pdb


from imageProcessing import processPFAS
from results import write_results


StripResult = collections.namedtuple('StripResult', 'string min_conf')


INPUT_FILENAME = 'newAItestdata.png'

SHOW_IMAGES = False

MIN_HEIGHT_THRESHOLD = 60  # 20% of strip height


def process_strip(strip):
    """FINISH ADAPTING THIS!!!"""

    # convert PIL image to opencv gray and apply Gaussian filtering
    pil_rgb = strip.convert('RGB')
    opencv_rgb = np.array(pil_rgb)
    im_bgr = cv2.cvtColor(opencv_rgb, cv2.COLOR_RGB2BGR)
    im_gray = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

    # Threshold the image
    ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the image
    ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    # Get rectangles contains each contour
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]

    min_conf = 1.0
    string = ''

    # For each rectangular region, calculate HOG features and predict
    # the digit using Linear SVM.
    for rect in sorted(rects, key=lambda rect: rect[0]):

        height = rect[3]
        if height < MIN_HEIGHT_THRESHOLD:
            continue

        # Make the rectangular region around the digit
        leng = int(rect[3] * 1.6)
        pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
        pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
        roi = im_th[pt1:pt1+leng, pt2:pt2+leng]

        # Resize the image
        try:
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3, 3))

            # Calculate the HOG features
            roi_hog_fd = hog(
                    roi, orientations=9, pixels_per_cell=(14, 14),
                    cells_per_block=(1, 1), visualise=False
                    )

        except:
            character = '?'

        else:
            features = np.array([roi_hog_fd], 'float64')
            nbr = clf.predict(features)
            character = str(int(nbr[0]))
            #probs = clf.predict_proba(features)

        string += character
        #conf = probs[0]
        #min_conf = min(min_conf, 

        if SHOW_IMAGES:
            # Draw the rectangles
            cv2.rectangle(im_gray, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
            cv2.putText(im_gray, character, (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

    if SHOW_IMAGES:
        plt.imshow(im_gray, interpolation='bicubic')
        #cv2.imshow("Resulting Image with Rectangular ROIs", im_gray)
        #cv2.waitKey()

    return StripResult(string, min_conf)


def process_strips(strips):
    """Process strips dict to create results dict.

    strips is a dict that contains (at least):

        - an entry for each question, mapping the question's name (as a
          string) to an image strip (as a PIL Image object) corresponding
          to the student's answer, and

        - an entry for the student's ID, mapping "StudentID" to an image
          strip (again, as a PIL Image object) corresponding to the
          student's handwritten ID.

    The returned dict contains the corresponding entries, but with the
    strips replaced with the corresponding recognized text as stings.

    """
    results = {}

    sid_results = process_strip(strips['StudentID'])
    sid_string = sid_results.string
    sid_min_conf = sid_results.min_conf

    results['StudentID'] = {
            'answer': sid_string,
            'min_conf': sid_min_conf
            }

    results['questions'] = {}
    for question, strip in strips['questions'].items():
        print('Processing question #{}'.format(question))
        try:
            strip_results = process_strip(strip)
        except Exception as e:
            pdb.set_trace()
            string = 'ERROR'
            min_conf = 0
        else:
            string = strip_results.string
            min_conf = strip_results.min_conf

        results['questions'][question] = {
                'answer': string,
                'min_conf': min_conf
                }

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pfas')
    parser.add_argument('output')

    args = parser.parse_args()
    pfas_filename = args.pfas
    output = args.output

    # Load the classifier
    clf = joblib.load("digits_cls.pkl")

    strips = processPFAS(pfas_filename)
    results = process_strips(strips)

    if SHOW_IMAGES:
        plt.show()
    write_results(output, results)
