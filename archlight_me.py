# import the necessary packages
from PIL import Image, ImageEnhance
import pytesseract
import argparse
import cv2
import os
import imageSearch
import time
import pyautogui
from time import gmtime, strftime


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
    try:
        return eval(text)
    except:
        return None



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

    # Successfull OCR always gives an array with 5 elements.
    if len(arr) == 5:
        return arr
    else:
        return None

def getOptionCords(img, number):
    img = cv2.imread(img)
    height, width, channels = img.shape
    return int((height/5) * number - (height/5)/2)

def findEssenceVerification():
    verificationPos = imageSearch.imagesearch("assets/please.png")
    return verificationPos

def screenShot(x1, y1, x2, y2, name):
    img = imageSearch.region_grabber(region=(x1, y1, x2, y2))
    img.save(name)


def keyPress(key):
    pyautogui.keyDown(key)
    print("pressing down: ", key)
    pyautogui.keyUp(key)

def chooseOption(num, x ,y):
    optionY = getOptionCords("tmpOptions.png", num)
    pyautogui.moveTo(x+15, y+optionY)
    pyautogui.click(button="left")
    pyautogui.press('enter')
    pyautogui.press('enter')


def foundEssence(essence):
    #print("Please pos: ", essence[0], essence[1])
    #print("tmpQuestion loc: ", essence[0], essence[1]+15, essence[0]+45, essence[1]+25)
    #print("tmpOptions loc: ", essence[0], essence[1]+30, essence[0]+45, essence[1]+100)
    screenShot(essence[0], essence[1]+15, essence[0]+45, essence[1]+25, "tmpQuestion.png")
    question = getTasseractQuestion("tmpQuestion.png")
    print("problem: ", question)
    if question is not None:
        screenShot(essence[0], essence[1]+30, essence[0]+45, essence[1]+100, "tmpOptions.png")
        optionArr = getTasseractOptions("tmpOptions.png")
        if optionArr is not None:
            print("options: ", optionArr)
            k = 1
            for option in optionArr:
                if int(option) == question:
                    chooseOption(k, essence[0], essence[1]+30)
                else:
                    k += 1
            return True
        else:
            return False
    else:
        return False

def main():
    try:
        print("Waiting for essence..")
        essencesFound = 0
        while True:
            essence = findEssenceVerification()
            if essence[0] != -1:
                success = foundEssence(essence)
                if success:
                    essencesFound += 1
                    cTime = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
                    print("{0} - You have now found: {1} monster essence(s).".format(cTime, essencesFound))
                    print("Waiting for essence..")
                else:
                    print("Question or problem OCR failed, still looking..")
                    time.sleep(5)
                essence = (-1, -1) # reset
            else:
                time.sleep(5)
    except KeyboardInterrupt:
        print("Stopped running due to KeyboardInterrupt")

main()
