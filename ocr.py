# import the necessary packages
from PIL import Image, ImageEnhance
import pytesseract
import argparse
import cv2
import os
import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())


# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
	# gray = cv2.medianBlur(gray, 3)


# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
# tessedit_char_whitelist=0123456789+
config = ('--psm 6 --oem 0 -c tessedit_char_whitelist=0123456789+')
text = pytesseract.image_to_string(Image.open(filename), lang='eng', config=config)
textOrg = pytesseract.image_to_string(Image.open(args["image"]), lang='eng', config=config)

os.remove(filename)
print("grey:", text)
print("original: ", textOrg)

arr = []
for line in text.splitlines():
    arr.append(line)

arr = list(filter(None, arr))
print(arr)

# show the output images
cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)
#python .\ocr.py -i problem.png --preprocess "blur"
