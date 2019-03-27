from lib import imageSearch as imgS
import pyautogui
import win32api, win32con, win32gui
from ctypes import windll
import time
import numpy as np
from PIL import Image
import cv2 as cv
import os
from lib import sendInput


def has_cd(img, x, y, im=None):
    img = 'assets/cds/{}.png'.format(img)
    no_cd = imgS.imagesearcharea(img, x, y, x+50, y+50, 0.7, im)
    if no_cd[0] is not -1:
        #it has no cd, return false
        return False
    else:
        return True

'''
Updating all cd's yourself is too much work.

input:
gui: this is everything, alright

result:
looping through all .png files in "assets/cds/", doing an imagesearch and updating its location in .ini file.
'''
def find_cds(gui):
    for item in gui.config.items('SPELL_NAME'):
        directory_in_str = "assets/cds/"
        directory = os.fsencode(directory_in_str)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".png"):
                spell = filename.replace(".png", "")
                if item[1].replace(" ", "_") == spell:
                    print(item[0])
                    if gui.config.has_option('ATTACK_COOLDOWNS', item[0]):
                        coords = imgS.imagesearch(directory_in_str + filename)
                        print(coords)
                        if coords[0] is not -1:
                            gui.config.set('ATTACK_COOLDOWNS', item[0], str(coords))
                    elif gui.config.has_option('HEALING_COOLDOWNS', item[0]):
                        coords = imgS.imagesearch(directory_in_str + filename)
                        if coords[0] is not -1:
                            gui.config.set('HEALING_COOLDOWNS', item[0], str(coords))
                    elif gui.config.has_option('SUPPORT_COOLDOWNS', item[0]):
                        coords = imgS.imagesearch(directory_in_str + filename)
                        if coords[0] is not -1:
                            gui.config.set('SUPPORT_COOLDOWNS', item[0], str(coords))
    gui.update_config()


def get_monster_list(gui):
    targets = gui.config.get('MONSTERS', 'list').split(', ')
    targets = map(lambda target:target.replace(" ", "_"), targets)
    targets = map(lambda target: 'assets/monsters/'+target+'.png', targets)
    return list(targets)

def get_friend_list(gui):
    names = gui.config.get('HEAL_FRIEND', 'names').split(', ')
    friends = map(lambda friend:friend.replace(" ", "_"), names)
    return list(friends)



# Code to check if left or right mouse buttons were pressed

def detect_mouse_click(arg):
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

    while True:
        a = win32api.GetKeyState(0x01)

        if a != state_left:  # Button state changed
            state_left = a

            if a < 0:
                #print('Left Button Pressed')
                coords = pyautogui.position()
                return coords

    time.sleep(0.001)


def string2tuple(old_string):
    new_tuple = tuple(int(x) for x in old_string[1:-1].split(','))
    return new_tuple



def key2hex(key):
    if key == 'F1' or key == 'f1':
        key = hex(ord(';'))
    elif key == 'F2' or key == 'f2':
        key = hex(ord('<'))
    elif key == 'F3' or key == 'f3':
        key = hex(ord('='))
    elif key == 'F4' or key == 'f4':
        key = hex(ord('>'))
    elif key == 'F5' or key == 'f5':
        key = hex(ord('?'))
    elif key == 'F6' or key == 'f6':
        key = hex(ord('@'))
    elif key == 'F7' or key == 'f7':
        key = hex(ord('A'))
    elif key == 'F8' or key == 'f8':
        key = hex(ord('B'))
    elif key == 'F9' or key == 'f9':
        key = hex(ord('C'))
    elif key == 'F10' or key == 'f10':
        key = hex(ord('D'))
    elif key == 'F11' or key == 'f11':
        key = hex(122)
    elif key == 'F12' or key == 'f12':
        key = hex(123)
    elif key == 'Del' or key == 'DEL' or key == 'del':
        key = hex(ord('S'))
    elif key == 'Ins' or key == 'INS' or key == 'ins':
        key = hex(ord('R'))
    elif key == 'Home' or key == 'HOME' or key == 'home':
        key = hex(ord('G'))
    elif key == 'End' or key == 'END' or key == 'end':
        key = hex(ord('O'))
    elif key == 'PgUp' or key == 'PGUP' or key == 'pgup' or key == 'Pgup':
        key = hex(ord('I'))
    elif key == 'PgDn' or key == 'PGDN' or key == 'pgdn' or key == 'Pgdn':
        key = hex(ord('Q'))

    hex_int = int(key, 16)
    return hex_int

def find_battlelist():
    battlelist_start = imgS.imagesearch('assets/battlelist/battlelist.png')
    if battlelist_start[0] is not -1:
        x2, y2 = pyautogui.size()
        battlelist_end = imgS.imagesearcharea('assets/battlelist/minimize_close.png', battlelist_start[0], battlelist_start[1], x2, y2)
        if battlelist_end[0] is not -1:
            battlelist_end = (battlelist_end[0] + battlelist_start[0], y2) #relative to absolute
            return [battlelist_start, battlelist_end]
    return [-1, -1]

def RGB_deviations(color, end_bar_color, pixel, deviation):
    R = pixel[0:1]
    G = pixel[1:2]
    B = pixel[2:3]
    # print("RGB: {0}, {1}, {2}     color: {3}".format(R,G,B, color))
    # print("R: {0} - {1} = {2} deviation {3}".format(color[0], R, color[0]-R, deviation))
    # print("G: {0} - {1} = {2} deviation {3}".format(color[1], G, color[1]-G, deviation))
    # print("B: {0} - {1} = {2} deviation {3}".format(color[2], B, color[2]-B, deviation))
    if color[0] - R >= -deviation and color[0] - R <= deviation:
        if color[1] - G >= -deviation and color[1] - G <= deviation:
            if color[2] - B >= -deviation and color[2] - B <= deviation:
                return True

    if R == end_bar_color[0]:
        if G == end_bar_color[1]:
            if B == end_bar_color[2]:
                # we are at full HP or mana
                return True
    return False

'''
optimize by changing loop to ... algo
look at half recursivly to find value. O(n/2).
atm O(n)


what the ... have I done here? Why not run the method twice instead of inputting 2 different colors? brain fart confirmed.
'''
def find_pixel_color(color, end_bar_color, deviation, x1, y1, x2, y2, image=None):
    #template = cv2.imread(image, 0)
    # print("called with:", color, end_bar_color, deviation, x1, y1, x2, y2)
    if image is None:
        image = imgS.region_grabber((x1, y1, x2, y2))
    im = np.array(image)
    #image.save('hp.png')
    rows = im.shape[0]
    cols = im.shape[1]
    for i in range(rows):
        for j in range(cols):
            pixel = im[i, j]
            # pyautogui.moveTo(j+x1, i+y1)
            if RGB_deviations(color, end_bar_color, pixel, deviation):
                match = (int(j+x1+1), int(i+y1))
                # pyautogui.moveTo(j+x1, i+y1)
                return match
    no_match = (-1, -1)
    return no_match

def dev_find_color(x1, y1, x2, y2):
    image = imgS.region_grabber((x1, y1, x2, y2))
    im = np.array(image)
    image.save('find_color_area.png')
    rows = im.shape[0]
    cols = im.shape[1]
    for i in range(rows):
        for j in range(cols):
            pixel = im[i, j]
            print(pixel)
            pyautogui.moveTo(j+x1, i+y1)

def find_countours(im):
    # Convert image to gray and blur it
    src_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    src_gray = cv.blur(src_gray, (3,3))

    # Create Window
    # source_window = 'Source'
    # cv.namedWindow(source_window)
    # cv.imshow(source_window, im)
    threshold = 100 # initial threshold
    # Detect edges using Canny
    canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    # Find contours
    _, contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Draw contours
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (255, 255, 255)
        cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)
    # Show in a window
    # cv.imshow('Contours', drawing)
    # Save 1px thick line
    something, drawing_w, drawing_h = drawing.shape[::-1]
    middle_height = int(drawing_h/2)
    crop_drawing = drawing[middle_height-1:middle_height+1, 0:drawing_w]
    # cv.imwrite('tmp/contours.png', crop_drawing)
    # cv.waitKey() #awsome debugging tool
    return crop_drawing



def setFocusWindow(gui):
    '''sets focus'''
    whndl = sendInput.get_whndl(gui.title)
    win32gui.SetForegroundWindow(whndl)
