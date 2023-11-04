"""This module is everything regarding healing and finding hp / mana values."""
import random
import time
from collections import defaultdict
import traceback
import numpy as np
import pyautogui
import cv2
from lib import imageSearch as imgS
from lib import utilities, sendInput
from engine import healFriend
from PIL import Image

random.seed()
NEXT_TIME = time.time()

COLOR_DICT = {
    'hp': [102, 126, 109, 108],
    'hp_end_bar': [61, 59, 62, 63],
    'mp': [108, 96, 93, 94],
    'mp_end_bar': [73, 64]} 


START_COORDS_DICT = defaultdict(list)
END_COORDS_DICT = defaultdict(list)
STATUS_BAR_DICT = defaultdict(list)


def append_dict(dict, key, values):
    '''stores {key: [x, y]}'''
    for item in values:
        if item not in dict[key]:
            dict[key].append(item)

def pixels2percent(start, end, current):
    '''converts pixels to a percentage.'''
    total = end - start
    to_pc = total / 100
    current_pc = (current - start) / to_pc
    return current_pc

def find_hp(gui):
    '''finds the location (pixels) of the health bar'''
    image = 'assets/life_obs.png'
    x_end, y_end = pyautogui.size()
    x_start = (x_end / 5) * 4
    coords_relative = imgS.imagesearcharea(image, x_start, 0, x_end, y_end, gui.currentImage)
    hp_colors = COLOR_DICT['hp'] # gray scale hp
    hp_bar_end_color = COLOR_DICT['hp_end_bar']
    if coords_relative[0] is not -1:
        coords = [coords_relative[0] + x_start, coords_relative[1]]
        hp_start = None
        hp_end = None
        
        im = gui.currentImage[int(coords[1]+4):int(coords[1]+5), int(coords[0]):int(x_end)]
        pointer = None
        for index, pixelVal in enumerate(im[0]):
            if pixelVal in hp_colors:
                hp_start = int(coords[0]) + index
                append_dict(START_COORDS_DICT, 'hp', [hp_start, coords[1]+4])
                pointer = index
                break

        for index, pixelVal in enumerate(im[0][pointer:]):
            if pixelVal in hp_bar_end_color:
                hp_end = int(coords[0]) + index + pointer
                append_dict(END_COORDS_DICT, 'hp', [hp_end, coords[1]+5])
                break


def find_status_bar(gui):
    # stupid, just look for the stop button
    '''finds the status bar below equipment'''
    image = 'assets/statusbar/left_corner_obs.png'
    img = cv2.imread(image, 0)
    img_w, img_h = img.shape[::-1]
    x2, y2 = pyautogui.size()
    x1 = int((x2 / 5) * 4)
    para_coords = imgS.imagesearcharea(image, x1, 0, x2, y2, gui.currentImage)
    if para_coords[0] is not -1:
        append_dict(STATUS_BAR_DICT, 'start', [para_coords[0] + x1, para_coords[1] + int(img_h / 2)])
        append_dict(STATUS_BAR_DICT, 'end', [para_coords[0] + x1 + 100, para_coords[1] + int(img_h / 2) + 1])



def find_mp(gui):
    '''finds the location (pixels) of the mana bar'''
    image = 'assets/mana_obs.png'
    x2, y2 = pyautogui.size()
    x1 = (x2 / 5) * 4
    coords_relative = imgS.imagesearcharea(image, x1, 0, x2, y2, gui.currentImage)
    mp_colors = COLOR_DICT['mp'] # gray scale mp
    mp_bar_end_color = COLOR_DICT['mp_end_bar']


    if coords_relative[0] is not -1:
        coords = [coords_relative[0] + x1, coords_relative[1] + 1]  #add back offset
        # utilities.dev_find_color(coords[0], coords[1], x2-100, coords[1]+1)
        mp_start = None
        mp_end = None
        im = gui.currentImage[int(coords[1]+4):int(coords[1]+5), int(coords[0]):int(x2)]
        img = Image.fromarray(im)
        img.save("your_file.jpeg")
        pointer = None
        for index, pixelVal in enumerate(im[0]):
            if pixelVal in mp_colors:
                mp_start = int(coords[0]) + index
                append_dict(START_COORDS_DICT, 'mp', [mp_start, coords[1]+4])
                pointer = index
                break


        for index, pixelVal in enumerate(im[0][pointer:]):
            if pixelVal in mp_bar_end_color:
                mp_end = int(coords[0]) + index + pointer
                append_dict(END_COORDS_DICT, 'mp', [mp_end, coords[1]+5])
                break




def get_curr(empty_key, im):
    '''finds the current hp and returns it as %'''
    startT = time.time()
    start = START_COORDS_DICT[empty_key[0:2]]
    end = END_COORDS_DICT[empty_key[0:2]]
    color = COLOR_DICT[empty_key]

    if start != [] and end != []:
        for index, pixel in enumerate(im[start[1]:end[1], start[0]:end[0]][0]):
            if not pixel in color:
                current_pc = pixels2percent(start[0], end[0], start[0]+index)
                if current_pc is None:
                    current_pc = 0
                return int(current_pc)
    else:
        print("Couldn't find start or end anchor for hp/mp, try restarting. \n \
        Are 'show status bar' toggled in Tibia options? \n \
        Advanced settings, Interface -> HUD at the bottom. \n \n \
        if you are running several monitors its possible we are looking at another monitor.")



def check_para(gui):
    '''checking status bar for paralyze'''
    config = gui.config
    start = STATUS_BAR_DICT['start']
    end = STATUS_BAR_DICT['end']
    para_color = [109, 27, 27]
    deviation = 10
    if STATUS_BAR_DICT['start'] != [] and STATUS_BAR_DICT['end'] != []:
        paralyzed = utilities.find_pixel_color(para_color, para_color, deviation, start[0], start[1], end[0], end[1], gui.currentImage)
        if paralyzed[0] is not -1:
            heal(config.get('SAVED_HOTKEYS', 'anti_paralyze'), gui)
    else:
        print("Couldn't fint status bar, trying to find it.. \n Is it visible?")
        print("status bar dict: ", STATUS_BAR_DICT)
        find_status_bar()

# [129 24 23]
# [144 20 20]
# [109 27 27]
# [248 1 1]
# [255 0 0]
# [233 4 4]
# [94 27 27]
# [144 18 19]
def find_anchors(gui):
    '''finding location of stuff by using image search.'''
    find_hp(gui)
    find_mp(gui)
    find_status_bar(gui)
    print("ANCHORS", START_COORDS_DICT, END_COORDS_DICT)
    return START_COORDS_DICT, END_COORDS_DICT

def run(gui):
    '''runs this module'''
    # start = time.time()
    heal_engine(gui)
    # end = time.time()
    # print("time to find hp, mana: ", end-start)
def heal(hotkey, gui):
    '''send heal'''
    sendInput.send_key(hotkey, title=gui.title)
    time.sleep(random.uniform(0.15, 0.4))

def heal_engine(gui):
    '''healing conditions'''
    try:
        hp = get_curr('hp', gui.currentImage)
        mp = get_curr('mp', gui.currentImage)
        gui.player.hp = hp
        gui.player.mp = mp
        config = gui.config
        if hp is None:
            hp = 100
        if mp is None:
            mp = 100
        if hp is not None and mp is not None:
            ### HEALTH POTS ###
            if hp < config.getint('SAVED_VALUES', 'low_health_potion') and \
                gui.all_bools['low_health_potion'].get():
                heal(config.get('SAVED_HOTKEYS', 'low_health_potion'), gui)
            elif hp < config.getint('SAVED_VALUES', 'high_health_potion') and \
                gui.all_bools['high_health_potion'].get():
                heal(config.get('SAVED_HOTKEYS', 'high_health_potion'), gui)
            ### MANA POTION ###
            elif mp < config.getint('SAVED_VALUES', 'low_mana_potion') and \
                gui.all_bools['low_mana_potion'].get():
                heal(config.get('SAVED_HOTKEYS', 'low_mana_potion'), gui)
            elif mp < config.getint('SAVED_VALUES', 'high_mana_potion') and \
                gui.all_bools['high_mana_potion'].get():
                global NEXT_TIME
                if time.time() > NEXT_TIME:
                    heal(config.get('SAVED_HOTKEYS', 'high_mana_potion'), gui)
                    NEXT_TIME = time.time() + 1.5 # 1,5s imaginary cooldown
            ### SPELL HEALING ### !!!!  LOW_HP -> SIO if active -> HIGH HEALING
            if hp < config.getint('SAVED_VALUES', 'low_spell_healing') and \
                gui.all_bools['low_spell_healing'].get():
                heal(config.get('SAVED_HOTKEYS', 'low_spell_healing'), gui)
            elif gui.checkButton_hk_bools['heal_friend'].get() is True:
                names = utilities.get_friend_list(gui)
                for name in names:
                    healFriend.heal_friend(gui, name)
            elif hp < config.getint('SAVED_VALUES', 'high_spell_healing') and gui.all_bools['high_spell_healing'].get():
                heal(config.get('SAVED_HOTKEYS', 'high_spell_healing'), gui)
            
            ### LAST PRIORITY CHECK PARA ###
            if gui.all_bools['anti_paralyze'].get():
                check_para(gui)

        print("hppc: {}   mppc: {}".format(hp, mp))
            
    except Exception:
        print("exception: ", traceback.format_exc())




