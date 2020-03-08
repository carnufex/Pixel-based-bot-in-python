"""This module is everything regarding healing and finding hp / mana values."""
import random
import time
from collections import defaultdict
import pyautogui
import cv2
from lib import imageSearch as imgS
from lib import utilities, sendInput
from engine import healFriend

random.seed()
NEXT_TIME = time.time()

COLOR_DICT = {'hp': [219, 79, 79],
              'hp_empty': [77, 90, 116],
              'hp_end_bar': [47, 51, 62],
              'hp_full': [100, 46, 49],
              'mp': [101, 98, 240],
              'mp_empty': [89, 95, 106],
              'mp_end_bar': [51, 52, 56],
              'mp_full': [83, 80, 192]}


START_COORDS_DICT = defaultdict(list)
END_COORDS_DICT = defaultdict(list)
STATUS_BAR_DICT = defaultdict(list)


def append_dict(dict, key, values):
    '''work around to have dicts with 1 key and multiple values. stores {key: [x, y]}'''
    for item in values:
        if item not in dict[key]:
            dict[key].append(item)

def pixels2percent(start, end, current):
    '''converts pixels to a percentage.'''
    total = end - start
    to_pc = total / 100
    current_pc = (current - start) / to_pc
    return current_pc

def find_hp():
    '''finds the location (pixels) of the health bar'''
    image = 'assets/life.png'
    img = cv2.imread(image, 0)
    img_w, img_h = img.shape[::-1]
    x_end, y_end = pyautogui.size()
    x_start = (x_end/5) * 4
    screen_shot = imgS.region_grabber((x_start, 0, x_end, y_end))
    screen_shot.save('test.jpg')
    coords_relative = imgS.imagesearcharea(image, x_start, 0, x_end, y_end, im=screen_shot)
    if coords_relative[0] is not -1:
        coords = [coords_relative[0]+x_start+img_w, coords_relative[1]+5] #add back offset
        hp_start = utilities.find_pixel_color(COLOR_DICT['hp'], COLOR_DICT['hp_full'], 0,\
            coords[0], coords[1], x_end, y_end)
        if hp_start[0] is not -1:
            append_dict(START_COORDS_DICT, 'hp', hp_start)
            hp_end = utilities.find_pixel_color(COLOR_DICT['hp_end_bar'], COLOR_DICT['hp_full'], 0,\
                hp_start[0], hp_start[1], x_end, y_end)
            if hp_end[0] is not -1:
                append_dict(END_COORDS_DICT, 'hp', hp_end)

def find_status_bar():
    '''finds the status bar below equipment'''
    image = 'assets/statusbar/left_corner.png'
    img = cv2.imread(image, 0)
    img_w, img_h = img.shape[::-1]
    x2, y2 = pyautogui.size()
    x1 = int((x2/5)*4)
    para_coords = imgS.imagesearcharea(image, x1, 0, x2, y2)
    if para_coords[0] is not -1:
        append_dict(STATUS_BAR_DICT, 'start', [para_coords[0] + x1, para_coords[1] + int(img_h/2)])
        append_dict(STATUS_BAR_DICT, 'end', [para_coords[0] + x1 + 100, para_coords[1] + int(img_h/2) + 1])



def find_mp():
    '''finds the location (pixels) of the mana bar'''
    image = 'assets/mana.png'
    img = cv2.imread(image, 0)
    img_w, img_h = img.shape[::-1]
    x2, y2 = pyautogui.size()
    x1 = (x2/5) * 4
    im = imgS.region_grabber((x1, 0, x2, y2))
    coords_relative = imgS.imagesearcharea(image, x1, 0, x2, y2, im=im)
    if coords_relative[0] is not -1:
        coords = [coords_relative[0]+x1+img_w, coords_relative[1]+5]  #add back offset
        mp_start = utilities.find_pixel_color(COLOR_DICT['mp'], COLOR_DICT['mp_full'], 0, coords[0], coords[1], x2, coords[1]+1)
        if mp_start[0] is not -1:
            append_dict(START_COORDS_DICT, 'mp', mp_start)
            mp_end = utilities.find_pixel_color(COLOR_DICT['mp_end_bar'], COLOR_DICT['mp_full'], 0, mp_start[0], mp_start[1], x2, mp_start[1]+1)
            if mp_end[0] is not -1:
                append_dict(END_COORDS_DICT, 'mp', mp_end)



def get_curr(empty_key, deviation):
    '''finds the current hp and returns it as %'''
    start = START_COORDS_DICT[empty_key[0:2]]
    end = END_COORDS_DICT[empty_key[0:2]]
    color = COLOR_DICT[empty_key]
    # print("start: {0}   end: {1}    color: {2}".format(start, end, color))
    if start != [] and end != []:
        current_px = utilities.find_pixel_color(color, COLOR_DICT[empty_key[0:2]+'_full'], deviation, start[0], start[1], end[0], start[1]+1) #change end[1] to start[1]+1?
        if current_px[0] is not -1:
            current_pc = pixels2percent(start[0], end[0], current_px[0])
            return int(current_pc)
        return None
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
        paralyzed = utilities.find_pixel_color(para_color, para_color, deviation, start[0], start[1], end[0], end[1])
        if paralyzed[0] is not -1:
            heal(config.get('SAVED_HOTKEYS', 'anti_paralyze'), gui)
    else:
        print("Couldn't fint status bar, trying to find it.. \n Is it visible?")
        print("status bar dict: ", STATUS_BAR_DICT)
        find_status_bar()

# [129  24  23]
# [144  20  20]
# [109  27  27]
# [248   1   1]
# [255   0   0]
# [233   4   4]
# [94 27 27]
# [144  18  19]

def find_anchors():
    '''finding location of stuff by using image search.'''
    find_hp()
    find_mp()
    find_status_bar()
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
    hp = get_curr('hp_empty', 10)
    mp = get_curr('mp_empty', 10)
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
        ### SPELL HEALING ### !!!! LOW_HP -> SIO if active -> HIGH HEALING
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

    # print("Heal_engine time: {0}        hppc: {1}   mppc: {2}".format(end - start, hp, mp))



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
