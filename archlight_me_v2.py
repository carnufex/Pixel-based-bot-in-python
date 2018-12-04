# import the necessary packages
from PIL import Image, ImageEnhance
import pytesseract
import argparse
import cv2
import os
import imageSearch
import time
import pyautogui
import ctypes

RESOLUTION_CONFIG = {
    'questionPc': (0.42890625, 0.46875, 0.446484375, 0.47569444444444444444444444444444),
    'optionsPc': (0.42890625, 0.47916666666666666666666666666667, 0.446484375, 0.52777777777777777777777777777778),
    'questionCords': (),
    'optionsCords': ()
}

# makes the pixel stuff % based
def fixResolution():
    user32 = ctypes.windll.user32
    x, y = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    RESOLUTION_CONFIG['questionCords'] = (
        int(RESOLUTION_CONFIG['questionPc'][0] * x),
        int(RESOLUTION_CONFIG['questionPc'][1] * y),
        int(RESOLUTION_CONFIG['questionPc'][2] * x),
        int(RESOLUTION_CONFIG['questionPc'][3] * y)
    )
    RESOLUTION_CONFIG['optionsCords'] = (
        int(RESOLUTION_CONFIG['optionsPc'][0] * x),
        int(RESOLUTION_CONFIG['optionsPc'][1] * y),
        int(RESOLUTION_CONFIG['optionsPc'][2] * x),
        int(RESOLUTION_CONFIG['optionsPc'][3] * y)
    )


def getTasseractQuestion(image):
    # load the example image and convert it to grayscale
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Make it 3 times larger and B&W
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    config = ('--psm 6 --oem 0 -c tessedit_char_whitelist=0123456789+')
    text = pytesseract.image_to_string(Image.open(filename), lang='eng', config=config)

    # Remove tmp file
    os.remove(filename)

    ### debugging tools
    # cv2.imshow("Output", gray)
    # cv2.waitKey(0)
    return eval(text)


def getTasseractOptions(image):
    # load the example image and convert it to grayscale
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Make it 3 times larger and B&W
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    config = ('--psm 6 --oem 0 -c tessedit_char_whitelist=0123456789+')
    text = pytesseract.image_to_string(Image.open(filename), lang='eng', config=config)

    # Remove tmp file
    os.remove(filename)
    # Put OCR lines in an array
    arr = []
    for line in text.splitlines():
        arr.append(line)

    # Remove blank lines
    arr = list(filter(None, arr))

    ### debugging tools
    # cv2.imshow("Output", gray)
    # cv2.waitKey(0)
    return arr

def getOptionCords(img, number):
    img = cv2.imread(img)
    height, width, channels = img.shape
    return int((height/5) * number - (height/5)/2)


def findEssenceVerification():
    verificationPos = imageSearch.imagesearch("assets/please.png")
    return verificationPos

def screenShot(regionTuple, name):
    img = imageSearch.region_grabber(region=regionTuple)
    img.save(name)


def keyPress(key):
    pyautogui.keyDown(key)
    print("pressing down: ", key)
    pyautogui.keyUp(key)

def chooseOption(num, x ,y):
    optionY = getOptionCords("tmpOptions.png", num)
    pyautogui.moveTo(x+15, y+optionY) # also adding 15px to the right to make sure we are not exactly on the border.
    pyautogui.click(button="left")
    time.sleep(3)
    pyautogui.press('enter')
    pyautogui.press('enter')


def foundEssence(essence):
    screenShot((RESOLUTION_CONFIG['questionCords']), "tmpQuestion.png")
    question = getTasseractQuestion("tmpQuestion.png")
    print("problem: ", question)
    screenShot((RESOLUTION_CONFIG['optionsCords']), "tmpOptions.png")
    optionArr = getTasseractOptions("tmpOptions.png")
    print("options: ", optionArr)
    k = 1
    for option in optionArr:
        if int(option) == question:
            print("blank")
            #chooseOption(k, essence[0], essence[1]+30)
        else:
            k += 1

def main():
    try:
        print("Initialized, waiting for essence..")
        fixResolution()
        essencesFound = 0
        while True:
            essence = findEssenceVerification()
            if essence[0] != -1:
                foundEssence(essence)
                essencesFound += 1
                print("You have now found: {} monster essences.".format(essencesFound))
                print("Waiting for essence..")
                essence = (-1, -1) # reset
            else:
                # print("Waiting for essence..")
                time.sleep(5)
    except KeyboardInterrupt:
        print("Stopped running due to KeyboardInterrupt")

main()
#getResolution()
