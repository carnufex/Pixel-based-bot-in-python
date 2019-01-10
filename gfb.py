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
#waypoints = ["checkmark-wpt.png", "questionmark-wpt.png", "exclimationmark-wpt.png", "cross-wpt.png"]
def initMinimap():
    minimapStart = imgS.imagesearch("assets/minimap.png", 0.8)
    minimapEnd = imgS.imagesearch("assets/minimap-end.png", 0.8)
    if (minimapStart[0] != -1) and (minimapEnd[0] != -1):
        return (minimapStart[0], minimapStart[1], minimapEnd[0], minimapEnd[1])
    else:
        return (-1,-1,-1,-1)

def findMonsters(targets, found, startX=0, startY=0, im=None):
    #print("finding monsters")
    x, y = pyautogui.size()
    if im == None:
        im = imgS.region_grabber(region=(x/5, 0, x-(x/5), y))
    for monster in targets:
        #print("current found: ", found)
        found_monster = imgS.imagesearcharea(monster, startX, startY, x-(x/5), y, 0.7, im)
        if found_monster[0] is not -1:
            #put black box over found entry to avoid finding duplicates.
            im_arr = np.asarray(im)
            cv2.rectangle(im_arr, found_monster, (found_monster[0]+50, found_monster[1]+30), color=(0,0,0), thickness=-1)
            im_arr = cv2.cvtColor(im_arr, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(im_arr)
            #debugging purposes
            #im.save("wtf.png")
            # cv2.imwrite("my.png",im_arr)
            # cv2.imshow("lalala", im_arr)
            # k = cv2.waitKey(0) # 0==wait forever
            found_monster = (int(found_monster[0]+x/5+46), found_monster[1]+50) # adding back pixels removed to improve imageSearch and adding some offset
            found.append(found_monster)
            findMonsters([monster], found, startX, found_monster[1], im)
    #print("list of found monsters: ", found)
    return found
    #time.sleep(1)

def find_and_remove(list, element):
    if element in list:
        list.remove(element)
        return list

def find_groups(list, radius):
    res = []
    index = 0
    for element in list:
        tmp = []
        tmp.append(element)
        index += 1
        for next in list[index:]:
            if next[0] - element[0] < radius and next[0] - element[0] > radius*-1:
                if next[1] - element[1] < radius/2 and next[1] - element[1] > (radius/2)*-1:
                    tmp.append(next)
        res.append(tmp)
    #print(res)
    return res

def find_best_coords(lista):
    # returns largest subsets in a sorted list
    if len(lista) > 0:
        lista.sort(key=len, reverse=True)
        return lista

def aim(list, min_monsters):
    tmp = []
    for group in list:
        x = 0
        y = 0
        count = len(group)
        if count >= min_monsters:
            for tuple in group:
                x += tuple[0]
                y += tuple[1]
            print("x: {0}   y: {1}      count: {2}".format(x/count,y/count,count))
            tmp.append((x/count, y/count))
    return (tmp)

def fire(coords):
    old_pos = pyautogui.position()
    pyautogui.moveTo(coords)
    pyautogui.press('f11')
    pyautogui.click(button="left")
    pyautogui.moveTo(old_pos)

def run(radius, min_monsters):
    x,y = pyautogui.size()
    start_x = int(x/5)
    found = []
    im = imgS.region_grabber(region=(start_x, 0, x-start_x, y))
    start = time.time()
    coords_list = findMonsters(targets, found, start_x, im=im)
    end = time.time()
    print("find monsters time:", end - start)
    if len(coords_list) is not 0:
        alternatives = find_groups(coords_list, radius)
        best = find_best_coords(alternatives)
        coords = aim(best, min_monsters)
        coords = coords[:2]
        if len(coords) is not 0:
            print(coords)
            for pos in coords:
                cooldown = utilities.has_cd('assets/runes/avalanche.png', im)
                if not cooldown:
                    fire(pos)





def main():
    while True:
        try:
            run(400, 2)
        except KeyboardInterrupt:
            break

#main()
