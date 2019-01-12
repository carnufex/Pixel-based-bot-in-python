import imageSearch as imgS
import time
import msvcrt
import pyautogui
import os
import cv2
import numpy as np
from PIL import Image
import math
import utilities

#targets = ["assets/monsters/hp_bar.png"]
targets = ["assets/monsters/troll.png", "assets/monsters/war_wolf.png", "assets/monsters/orc_rider.png", "assets/monsters/orc_spearman.png", \
          "assets/monsters/orc_warrior.png"]
#targets = ["assets/monsters/troll.png"]

'''

Searchs for an image within an area

input :

image : path to the image file (see opencv imread for supported types)
x1 : top left x value
y1 : top left y value
x2 : bottom right x value
y2 : bottom right y value
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
im : a PIL image, usefull if you intend to search the same unchanging region for several elements
offset_x : if the PIL image in different from the resolution u need to compensate back by adding offset.
offset_y : same as offset_x

returns :
an array of top left corner coordinates or [-1,-1] if not anything was found.

'''
def imagesearcharea_array(array, x1,y1,x2,y2, precision=0.8, im=None, offset_x=0, offset_y=0) :
    if im is None :
        im = region_grabber(region=(x1, y1, x2, y2))
        # im.save('testarea.png') #usefull for debugging purposes, this will save the captured region as "testarea.png"

    matches = []
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)


    for image in array:
        template = cv2.imread(image, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), -1)
            matches.append((pt[0] + offset_x, pt[1] + offset_y))
    #cv2.imwrite('res.png',img_rgb)
    if len(matches) < 1:
        return [-1, -1]
    return matches

def aim_gfb(list, radius):
    x = 0
    y = 0
    for element in list:
        x += element[0]
        y += element[1]
    x_c = x / len(list)
    y_c = y / len(list)
    tmp = []
    for coord in list:
        x_p = coord[0]
        y_p = coord[1]
        d = math.sqrt((x_p - x_c)**2 + (y_p - y_c)**2)
        tmp.append((d, coord))
    i = 0
    for distance in tmp:
        if distance[0] <= radius:
            i += 1

    if i != len(list):
        tmp = sorted(tmp, key=lambda l:l[0], reverse=True)
        tmp = tmp[1:]
        flatten_tmp = [item for sublist in tmp for item in sublist]
        return aim_gfb(flatten_tmp[1::2], radius)
    else:
        print("shooting at {0} monsters. Radius: {1}".format(i, radius))
        return ((x_c, y_c), i)


def fire(hotkey, coords):
    pyautogui.press(hotkey)
    pyautogui.click(x=coords[0], y=coords[1], button="left")


def run(radius, min_monsters):
    start = time.time()
    x,y = pyautogui.size()
    start_x = int(x/5)
    im = imgS.region_grabber(region=(start_x, 0, x-start_x, y))
    coords_list = imagesearcharea_array(targets, 0, 0, x-(x/5), y, 0.7, im=im, offset_x=start_x)
    if coords_list[0] is not -1:
        best = aim_gfb(coords_list, radius)
        if best[1] >= 2:
            fire('f11', best[0])
            end = time.time()
            print("total time:", end - start)
            #pyautogui.moveTo(best[0])
