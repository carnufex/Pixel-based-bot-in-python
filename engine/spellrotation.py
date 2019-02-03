from lib import imageSearch as imgS
import time
import msvcrt
import os
import cv2
import numpy as np
from PIL import Image
import math
from lib import utilities, sendInput

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
def imagesearcharea_array(array, x1,y1,x2,y2, precision=0.8, im=None) :
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
            matches.append((pt[0] + x1, pt[1] + y1))
    #cv2.imwrite('res.png',img_rgb)
    if len(matches) < 1:
        return [-1, -1]
    return matches

'''

Searchs for a coordinate that places as many coordinates as possible from list inside of a circle

input :

list : an array of coordinates [(x,y), ...]
radius : radius of the circle

returns :
best possible coordinate along with amount of hits. ((x,y), amount)

'''
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
        return ((x_c, y_c), i)


'''
Presses hotkey and then left clicks on coords
input :
hotkey : string with button name, e.g. 'f11'
coords : tuple containing (x,y)
'''
def fire(hotkey, coords, gui):
    sendInput.send_key(hotkey, title=gui.title)
    if coords is not 0:
        sendInput.send_click(coords[0], coords[1], gui.title)


def proximity(list, range, x1, y1, x2, y2):
    x_center = ((x2-x1)/2)+x1
    y_center = ((y2-y1)/2)+y1
    results = []
    for coord in list:
        x_point = coord[0]
        y_point = coord[1]
        distance = math.sqrt((x_point - x_center)**2 + (y_point - y_center)**2)
        if distance <= range:
            results.append(coord)
    return results


'''

'''
def spellrotation(start_coords, end_coords, gui, targets):
    start = time.time()
    config = gui.config
    active_spells = []


    im = imgS.region_grabber(region=(start_coords[0], start_coords[1], end_coords[0], end_coords[1]))
    coords_list = imagesearcharea_array(targets, start_coords[0], start_coords[1], end_coords[0], end_coords[1], 0.7, im=im)
    #look for all active spells and add them to active spell list along with priority
    for item in gui.all_spells_dict['attack']:
        item_tuple = (config['PRIORITY'][item], item)
        if gui.all_bools[item].get() is True:
            active_spells.append(item_tuple)
        elif item in active_spells:
            #spell has been toggled off, remove from active spells.
            active_spells.remove(item_tuple)

    active_spells.sort()
    for spell in active_spells:
        amount = int(config['AMOUNT'][spell[1]])
        hotkey = config['SAVED_HOTKEYS'][spell[1]]
        if coords_list[0] is not -1: #no monster on screen
            x1, y1 = utilities.string2tuple(gui.config.get('GAMEWINDOW', 'game_start_coords'))
            x2, y2 = utilities.string2tuple(gui.config.get('GAMEWINDOW', 'game_end_coords'))
            game_width = x2 - x1
            if spell[1] == 'aoe_rune':
                cooldown_coords = utilities.string2tuple(config['ATTACK_COOLDOWNS'][spell[1]])
                spell_name = config.get('SPELL_NAME', spell[1]).replace(" ", "_")
                cooldown = utilities.has_cd(spell_name, cooldown_coords[0], cooldown_coords[1])
                if not cooldown:
                    radius = (game_width * 0.35)
                    best = aim_gfb(coords_list, radius)
                    if best[1] >= amount:
                        fire(hotkey, best[0], gui)
                        end = time.time()
                        print("Spell rotation time: ", end-start)
                        break

            elif spell[1] == 'spell_1':
                cooldown_coords = utilities.string2tuple(config['ATTACK_COOLDOWNS'][spell[1]])
                spell_name = config.get('SPELL_NAME', spell[1]).replace(" ", "_")
                cooldown = utilities.has_cd(spell_name, cooldown_coords[0], cooldown_coords[1])
                if not cooldown:
                    radius = game_width * (0.15 * int(config.get('RANGE', spell[1])))
                    prox = proximity(coords_list, radius, x1, y1, x2, y2)
                    if len(prox) >= amount:
                        sendInput.send_key(hotkey, title=gui.title)
                        break

            elif spell[1] == 'spell_2':
                cooldown_coords = utilities.string2tuple(config['ATTACK_COOLDOWNS'][spell[1]])
                spell_name = config.get('SPELL_NAME', spell[1]).replace(" ", "_")
                cooldown = utilities.has_cd(spell_name, cooldown_coords[0], cooldown_coords[1])
                if not cooldown:
                    radius = game_width * (0.15 * int(config.get('RANGE', spell[1])))
                    prox = proximity(coords_list, radius, x1, y1, x2, y2)
                    if len(prox) >= amount:
                        sendInput.send_key(hotkey, title=gui.title)
                        break
