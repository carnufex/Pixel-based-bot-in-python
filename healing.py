import imageSearch as imgS
import pyautogui
import cv2
import numpy as np
from collections import defaultdict
import time
import sendInput

color_dict = { 'hp': [219, 79, 79],
                'hp_empty': [77,90,116],
                'hp_end_bar': [47, 51, 62],
                'hp_full': [100, 46, 49],
                'mp': [101, 98, 240],
                'mp_empty': [89, 95, 106],
                'mp_end_bar': [51, 52, 56],
                'mp_full': [83, 80, 192]
}


start_coords_dict = defaultdict(list)
end_coords_dict = defaultdict(list)

'''
go around to have dicts with 1 key and multiple values. stores {key: [x, y]}
'''
def append_dict(dict, key, values):
    for item in values:
        if item not in dict[key]:
            dict[key].append(item)

def pixels2percent(start, end, current):
    total = end - start
    to_pc = total / 100
    current_pc = (current - start) / to_pc
    return current_pc

def find_hp():
    image = 'assets/life.png'
    img = cv2.imread(image, 0)
    img_w, img_h = img.shape[::-1]
    x2, y2 = pyautogui.size()
    x1 = (x2/5) * 4
    im = imgS.region_grabber((x1, 0, x2, y2))
    coords_relative = imgS.imagesearcharea(image, x1, 0, x2, y2, im=im)
    if coords_relative[0] is not -1:
        coords = [coords_relative[0]+x1+img_w, coords_relative[1]+5] #add back offset
        hp_start = find_pixel_color(color_dict['hp'], color_dict['hp_full'], 0, coords[0], coords[1], x2, y2)
        if hp_start[0] is not -1:
            append_dict(start_coords_dict, 'hp', hp_start)
            hp_end = find_pixel_color(color_dict['hp_end_bar'], color_dict['hp_full'], 0, hp_start[0], hp_start[1], x2, y2)
            if hp_end[0] is not -1:
                append_dict(end_coords_dict, 'hp', hp_end)


def find_mp():
    image = 'assets/mana.png'
    img = cv2.imread(image, 0)
    img_w, img_h = img.shape[::-1]
    x2, y2 = pyautogui.size()
    x1 = (x2/5) * 4
    im = imgS.region_grabber((x1, 0, x2, y2))
    coords_relative = imgS.imagesearcharea(image, x1, 0, x2, y2, im=im)
    if coords_relative[0] is not -1:
        coords = [coords_relative[0]+x1+img_w, coords_relative[1]+5]  #add back offset
        mp_start = find_pixel_color(color_dict['mp'], color_dict['mp_full'], 0, coords[0], coords[1], x2, y2)
        if mp_start[0] is not -1:
            append_dict(start_coords_dict, 'mp', mp_start)
            mp_end = find_pixel_color(color_dict['mp_end_bar'], color_dict['mp_full'], 0, mp_start[0], mp_start[1], x2, y2)
            if mp_end[0] is not -1:
                append_dict(end_coords_dict, 'mp', mp_end)



def get_curr(empty_key, deviation):
    start = start_coords_dict[empty_key[0:2]]
    end = end_coords_dict[empty_key[0:2]]
    color = color_dict[empty_key]
    #print("start: {0}   end: {1}    color: {2}".format(start, end, color))
    if start is not [] and end is not []:
        current_px = find_pixel_color(color, color_dict[empty_key[0:2]+'_full'], deviation, start[0], start[1], end[0], end[1])
        if current_px[0] is not -1:
            current_pc = pixels2percent(start[0], end[0], current_px[0])
            return int(current_pc)
        return None


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
'''
def find_pixel_color(color, end_bar_color, deviation, x1, y1, x2, y2):
    #template = cv2.imread(image, 0)
    # print("called with:", color, end_bar_color, deviation, x1, y1, x2, y2)
    image = imgS.region_grabber((x1, y1, x2, y1+1))
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

def find_anchors():
    find_hp()
    find_mp()
    return start_coords_dict, end_coords_dict

    # for key, value in zip(start_coords_dict.items(), end_coords_dict.items()):
    #     print("key, value: ", key, value)
    #     if -1 in value or len(value) < 2:
    #         return False
    # return True

def run(gui):
    start = time.time()
    heal_engine(gui)
    end = time.time()
    #print("time to find hp, mana: ", end-start)

def heal(hotkey):
    sendInput.send_key(hotkey)

def heal_engine(gui):
    hp = get_curr('hp_empty', 10)
    mp = get_curr('mp_empty', 10)
    if hp is not None and mp is not None:
        if hp < int(gui.config['SAVED_VALUES']['low_healing']):
            heal(gui.config['SAVED_HOTKEYS']['low_healing'])
        elif mp < int(gui.config['SAVED_VALUES']['mana_pot']):
            print("mp < SAVED_VALUE mana_pot", mp, gui.config['SAVED_VALUES']['mana_pot'])
            heal(gui.config['SAVED_HOTKEYS']['mana_pot'])
        if hp < int(gui.config['SAVED_VALUES']['high_healing']):
            heal(gui.config['SAVED_HOTKEYS']['high_healing'])
    time.sleep(0.1)



# find_mp()

# RGB: [219], [79], [79]     color: [219, 79, 79]
# RGB: [219], [79], [79]     color: [219, 79, 79]
# RGB: [77], [89], [116]     color: [219, 79, 79]
# RGB: [61], [73], [101]     color: [219, 79, 79]
# RGB: [65], [78], [105]     color: [219, 79, 79]
# RGB: [72], [85], [112]     color: [219, 79, 79]
# RGB: [66], [78], [106]     color: [219, 79, 79]
# RGB: [69], [82], [110]     color: [219, 79, 79]
# RGB: [69], [82], [109]     color: [219, 79, 79]
# RGB: [68], [81], [108]     color: [219, 79, 79]
# RGB: [68], [81], [108]     color: [219, 79, 79]
# RGB: [72], [85], [113]     color: [219, 79, 79]
# RGB: [71], [83], [111]     color: [219, 79, 79]
# RGB: [66], [77], [101]     color: [219, 79, 79]
# RGB: [47], [51], [62]     color: [219, 79, 79]
# RGB: [73], [74], [74]     color: [219, 79, 79]
# RGB: [64], [64], [64]     color: [219, 79, 79]
# RGB: [69], [70], [70]     color: [219, 79, 79]
# RGB: [69], [70], [70]     color: [219, 79, 79]
