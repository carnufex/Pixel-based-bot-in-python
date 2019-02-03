from lib import imageSearch as imgS
import pyautogui, cv2, time
import numpy as np
from collections import defaultdict
from lib import utilities, sendInput
from engine import healFriend

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
        hp_start = utilities.find_pixel_color(color_dict['hp'], color_dict['hp_full'], 0, coords[0], coords[1], x2, y2)
        if hp_start[0] is not -1:
            append_dict(start_coords_dict, 'hp', hp_start)
            hp_end = utilities.find_pixel_color(color_dict['hp_end_bar'], color_dict['hp_full'], 0, hp_start[0], hp_start[1], x2, y2)
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
        mp_start = utilities.find_pixel_color(color_dict['mp'], color_dict['mp_full'], 0, coords[0], coords[1], x2, y2)
        if mp_start[0] is not -1:
            append_dict(start_coords_dict, 'mp', mp_start)
            mp_end = utilities.find_pixel_color(color_dict['mp_end_bar'], color_dict['mp_full'], 0, mp_start[0], mp_start[1], x2, y2)
            if mp_end[0] is not -1:
                append_dict(end_coords_dict, 'mp', mp_end)



def get_curr(empty_key, deviation):
    start = start_coords_dict[empty_key[0:2]]
    end = end_coords_dict[empty_key[0:2]]
    color = color_dict[empty_key]
    # print("start: {0}   end: {1}    color: {2}".format(start, end, color))
    if start is not [] and end is not []:
        current_px = utilities.find_pixel_color(color, color_dict[empty_key[0:2]+'_full'], deviation, start[0], start[1], end[0], end[1])
        if current_px[0] is not -1:
            current_pc = pixels2percent(start[0], end[0], current_px[0])
            return int(current_pc)
        return None
    else:
        print("Couldn't find current hp, try restarting. \n \
        Are 'show status bar' toggled in Tibia options? \n \
        Advanced settings, Interface -> HUD at the bottom")





def find_anchors():
    find_hp()
    find_mp()
    return start_coords_dict, end_coords_dict

def run(gui):
    start = time.time()
    heal_engine(gui)
    end = time.time()
    #print("time to find hp, mana: ", end-start)

def heal(hotkey, gui):
    sendInput.send_key(hotkey, title=gui.title)

def heal_engine(gui):
    hp = get_curr('hp_empty', 10)
    mp = get_curr('mp_empty', 10)
    config = gui.config
    if hp is not None and mp is not None:
        ### HEALTH POTS ###
        type = 'low_health_potion'
        if hp < config.getint('SAVED_VALUES', 'low_health_potion') and gui.all_bools['low_health_potion'].get():
            heal(config.get('SAVED_HOTKEYS', 'low_health_potion'), gui)
        elif hp < config.getint('SAVED_VALUES', 'high_health_potion') and gui.all_bools['high_health_potion'].get():
            heal(config.get('SAVED_HOTKEYS', 'high_health_potion'), gui)
        ### SPELL HEALING ### !!!! LOW_HP -> SIO if active -> HIGH HEALING
        if hp < config.getint('SAVED_VALUES', 'low_spell_healing') and gui.all_bools['low_spell_healing'].get():
            heal(config.get('SAVED_HOTKEYS', 'low_spell_healing'), gui)
        elif gui.checkButton_hk_bools['heal_friend'].get():
            names = gui.config.get('HEAL_FRIEND', 'names').split(', ')
            print(names)
            for name in names:
                healFriend.heal_friend(gui, name)
        elif hp < config.getint('SAVED_VALUES', 'high_spell_healing') and gui.all_bools['high_spell_healing'].get():
            heal(config.get('SAVED_HOTKEYS', 'high_spell_healing'), gui)
        ### MANA POTION ###
        if mp < config.getint('SAVED_VALUES', 'low_mana_potion') and gui.all_bools['low_mana_potion'].get():
            heal(config.get('SAVED_HOTKEYS', 'low_mana_potion'), gui)
        elif mp < config.getint('SAVED_VALUES', 'high_mana_potion') and gui.all_bools['high_mana_potion'].get():
            heal(config.get('SAVED_HOTKEYS', 'high_mana_potion'), gui)
            print("mp < SAVED_VALUE", mp, gui.config['SAVED_VALUES']['high_mana_potion'])
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
