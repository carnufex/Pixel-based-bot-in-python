from lib import utilities
from lib import imageSearch as imgS
import cv2 as cv
import os
import numpy as np
from lib import sendInput







#2 find friend to heal from battlelist
def find_player_name(img_path, coords, gui): #coords is array with tuples [(x_start, y_start), (x_end, y_end)]
    if os.path.isfile(img_path):
        # print("COORDS:", coords);
        # print(img_path, coords[0][0], coords[0][1], coords[1][0],
        # coords[1][1])
        x, y = imgS.imagesearcharea(img_path, coords[0][0], coords[0][1], coords[1][0], coords[1][1], gui.currentImage)
        if x is not -1:
            return [(coords[0][0] + x, coords[0][1] + y), (coords[1][0], coords[1][1])]
        else:
            return None
    else:
        print('There is no file "{0}" in assets/battlelist/friends/'.format(img_path))
        return [(-1, -1)]

#3 find friends hp
def find_player_hp(img_path, gui):
    # print("battle coords", battlelist_coords)
    coords = find_player_name(img_path, battlelist_coords, gui)
    if coords is not None:
        if coords[0][0] is not -1:
            img = cv.imread(img_path, 0)
            img_w, img_h = img.shape[::-1]
            hp_bar_size = 10 #px
            hp_bar_im = imgS.region_grabber((coords[0][0], coords[0][1] + img_h, coords[1][0], coords[0][1] + img_h + hp_bar_size))  # putting offset on x2 cuz im having troubles with scenarios with full hp
            img_rgb = np.array(hp_bar_im)
            return utilities.find_countours(img_rgb)
    return coords



#4 read friends hp
def friend_current_hp(img_path, gui):
    image = find_player_hp(img_path, gui)
    if image is not -1 and image is not None:
        something, image_w, image_h = image.shape[::-1]
        start_hp = utilities.find_pixel_color([255, 255, 255], [255, 255, 255], 0, 0, 0 ,0 ,0, image)
        if start_hp[0] is not -1:
            # -1 => not found or dead?
            current_hp = utilities.find_pixel_color([0, 0, 0], [0,0,0], 0, 0, 0 ,0 ,0, image)
            if current_hp[0] is not -1:
                # -1 => full HP or dead?
                to_percent = (image_w) / 100
                # returns % hp and putting on some offset since draw_contours
                # with line size 2 adds some to the actual hp
                return int((current_hp[0]) / to_percent)
        else:
            # I have problems finding borders on red HP, separating red RGB and
            # grey RGB is hard w/o converting it to HSV.
            # Only seems to occur on low HP; thus returning 1% hp for heals
            return 1

    return -1

#5 heal if conditions met
def heal_friend(gui, name):
    #1 find battlelist
    battlelist_coords = utilities.find_battlelist(gui)
    path = 'assets/battlelist/friends/{}.png'.format(name)
    hppc = friend_current_hp(path, gui)
    print("hppc: ", hppc)
    if hppc is not -1:
        if hppc < int(gui.config['HEAL_FRIEND']['friend_hp']):
            sendInput.send_key(gui.config['HEAL_FRIEND']['sio_hotkey'], title=gui.title)
            print("healed: ", name)

#5.0 friend is lower than X hp
#5.1 mana & hp above X, Y
#5.2 no CD


# heal_friend('war_wolf')
