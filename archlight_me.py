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
import threading


def get_tesseract_question(image):
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



def get_tesseract_options(image):
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

def get_option_coords(img, number):
    img = cv2.imread(img)
    height, width, channels = img.shape
    return int((height/5) * number - (height/5)/2)

def find_essence_verification():
    verificationPos = imageSearch.imagesearch("assets/please.png")
    return verificationPos

def screenshot(x1, y1, x2, y2, name):
    img = imageSearch.region_grabber(region=(x1, y1, x2, y2))
    img.save(name)


def choose_option(num, x ,y):
    optionY = get_option_coords("tmpOptions.png", num)
    pyautogui.moveTo(x+15, y+optionY)
    pyautogui.click(button="left")
    pyautogui.press('enter')
    pyautogui.press('enter')


def foundEssence(essence):
    #print("Please pos: ", essence[0], essence[1])
    #print("tmpQuestion loc: ", essence[0], essence[1]+15, essence[0]+45, essence[1]+25)
    #print("tmpOptions loc: ", essence[0], essence[1]+30, essence[0]+45, essence[1]+100)
    screenshot(essence[0], essence[1]+15, essence[0]+45, essence[1]+25, "tmpQuestion.png")
    question = get_tesseract_question("tmpQuestion.png")
    print("problem: ", question)
    if question is not None:
        screenshot(essence[0], essence[1]+30, essence[0]+45, essence[1]+100, "tmpOptions.png")
        optionArr = get_tesseract_options("tmpOptions.png")
        if optionArr is not None:
            print("options: ", optionArr)
            k = 1
            for option in optionArr:
                if int(option) == question:
                    choose_option(k, essence[0], essence[1]+30)
                else:
                    k += 1
            return True
        else:
            return False
    else:
        return False

def find_essence():
    found = False
    print("Waiting for essence..")
    while not found:
        pos = imageSearch.imagesearch_loop('assets/me.png', 1, 0.8)
        if pos[0] is not -1:
            print("found !me", pos)
            found = True
            pyautogui.press('f12')



def essence_bot(loop_delay):
    essence_count = 0
    try:
        while True:
            find_essence() # looping to find the green !me text.
            time.sleep(1)
            essence = find_essence_verification()
            if essence[0] != -1:
                success = foundEssence(essence)
                if success:
                    essence_count += 1
                    cTime = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
                    print("{0} - You have now found: {1} monster essence(s).".format(cTime, essence_count))
                    print("Waiting for essence..")
                else:
                    print("Question or problem OCR failed, still looking..")
                    time.sleep(loop_delay)
                essence = (-1, -1) # reset
            else:
                time.sleep(loop_delay)
    except KeyboardInterrupt:
        print("Stopped running due to KeyboardInterrupt")

def main():
    # Create two threads as follows
    essence_bot_thread = threading.Thread(target=essence_bot, args=(5,))
    try:
       essence_bot_thread.start()
    except:
       print("Error: unable to start thread")
main()
#imageSearch.find_rgb((40, 246, 13))
