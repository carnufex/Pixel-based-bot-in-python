'''cavebot'''
import time
import msvcrt
import os
import pyautogui
import cv2
from lib import imageSearch as imgS
from lib import sendInput, utilities
from engine import targeting, looting

# battlelist_coords = utilities.find_battlelist()

# WAYPOINTS = ["assets/map/checkmark.png", "assets/map/questionmark.png",
# "assets/map/exclimationmark.png", "assets/map/cross.png"]
WAYPOINTS = [{
        "mark": "checkmark",
        "type": "stand"
    },
    {
        "mark": "questionmark",
        "type": "stand"
    },
    {
        "mark": "exclimationmark",
        "type": "stand"
    },
    {
        "mark": "star",
        "type": "stand"
    },
    {
        "mark": "cross",
        "type": "stand"
    },
    {
        "mark": "church",
        "type": "stand"
    },
    {
        "mark": "mouth",
        "type": "stand"
    }]
def init_minimap(gui):
    '''finds map'''
    top_right = imgS.imagesearch("assets/map/minimap_settings.png", gui.currentImage, 0.8)
    map_size = 110 # 110px square
    minimap_start = (top_right[0] - map_size, top_right[1])
    minimap_end = (top_right[0], top_right[1] + map_size)
    if (top_right[0] != -1):
        return (minimap_start[0], minimap_start[1], minimap_end[0], minimap_end[1])
    return (-1, -1, -1, -1)


def go_wpt(wpt_img, minimap_pos, battlelist_coords, gui):
    '''click and move to wpt'''
    wpt = imgS.imagesearcharea("assets/map/" + wpt_img["mark"] + ".png", minimap_pos[0], minimap_pos[1], minimap_pos[2], minimap_pos[3], gui.currentImage, 0.7)
    if wpt[0] is not -1:
        target = targeting.has_targets(battlelist_coords)
        while target:
            print("killing something, sleeping")
            time.sleep(0.5)
            target = targeting.has_targets(battlelist_coords)
            if not target:
                # all targets dead, trigger looting
                looting.loot(gui)
        click_wpt(wpt_img, wpt, minimap_pos, gui.title)
        pressed = gui.checkButton_hk_bools['cavebot'].get()
        if not wpt_reached(wpt_img, minimap_pos) and pressed:
            go_wpt(wpt_img, minimap_pos, battlelist_coords, gui)
        else:
            if wpt_img["type"] != "stand":
                action_wpt(wpt_img, gui, minimap_pos, battlelist_coords)
    else:
        print("wpt not found: ", wpt_img)
    
def click_wpt(wpt_img, pos, minimap_pos, title):
    '''click wpt'''
    #imgS.click_image(wpt_img, (pos[0]+minimap_pos[0], pos[1]+minimap_pos[1]),
    #"left", 0)
    img = cv2.imread("assets/map/" + wpt_img["mark"] + ".png")
    height, width, channels = img.shape
    x = int(minimap_pos[0] + pos[0] + width / 2)
    y = int(pos[1] + height / 2)
    # print("clicking: ", x, y)
    sendInput.send_click(x, y, title)
    # pyautogui.moveTo(x, y)
    time.sleep(0.5)
    
def action_wpt(wpt, gui, minimap_pos, battlelist_coords):
    '''do action waypoint'''
    pos = utilities.string2tuple(gui.config.get('GAMEWINDOW', 'character_pos'))
    chase_off(gui.title)
    time.sleep(0.5)
    if wpt["type"] == 'rope':
        print("roping")
        sendInput.send_key('3', '3', title=gui.title)
        time.sleep(0.5)
        sendInput.send_click(pos[0], pos[1], title=gui.title)
        check = wpt_reached({"mark": "lock"}, minimap_pos)
        if not check:
            go_wpt(wpt, minimap_pos, battlelist_coords, gui)
        else:
            chase_on(gui.title)
    elif wpt["type"] == 'shovel':
        print('shoveling')
        start = utilities.string2tuple(gui.config.get('GAMEWINDOW', 'game_start_coords'))
        end = utilities.string2tuple(gui.config.get('GAMEWINDOW', 'game_end_coords'))
        offset_x = (end[0] - start[0]) / 15
        offset_y = (end[1] - start[1]) / 11
        sendInput.send_key('4', '4', title=gui.title)
        time.sleep(0.5)
        sendInput.send_click(pos[0], pos[1] - offset_y, title=gui.title)
        time.sleep(0.5)
        sendInput.send_click(pos[0], pos[1] - offset_y, title=gui.title)
        time.sleep(0.5)
        check = wpt_reached({"mark": "lock"}, minimap_pos)
        if not check:
            go_wpt(wpt, minimap_pos, battlelist_coords, gui)
        else:
            chase_on(gui.title)



def wpt_reached(wpt_img, minimap_pos):
    '''check if we reached wpt'''
    middle = 50
    middle_start = (minimap_pos[0] + middle, minimap_pos[1] + middle)
    middle_end = (minimap_pos[2] - middle, minimap_pos[3] - middle)
    wpt = imgS.imagesearcharea("assets/map/" + wpt_img["mark"] + ".png", middle_start[0], middle_start[1], middle_end[0], middle_end[1], gui.currentImage, 0.7)
    if wpt[0] is not -1:
        return True
    print("havent reached wpt: ", wpt_img)
    return False


def chase_off(title):
    '''turns chasing off'''
    image = "assets/stop_chase.png"
    x, y = pyautogui.size()
    x_start = x / 10 * 9
    follow_mode = imgS.imagesearcharea(image, x_start, 0, x, y, gui.currentImage)
    print("off: ", follow_mode)
    if follow_mode[0] is not -1:
        sendInput.send_click(follow_mode[0] + x_start, follow_mode[1] - 13, title)
        print("chase is off")
        time.sleep(0.5)
    

def chase_on(title):
    '''turns chasing on'''
    image = "assets/chase_target.png"
    x, y = pyautogui.size()
    x_start = x / 10 * 9
    follow_mode = imgS.imagesearcharea(image, x_start, 0, x, y)
    print("on: ", follow_mode)
    if follow_mode[0] is not -1:
        print("chase is on")
        sendInput.send_click(follow_mode[0] + x_start, follow_mode[1] - 13, title)
        time.sleep(0.5)

# def ss_wpt():
#     x,y = pyautogui.position()
#     ss = imgS.region_grabber((x, y, 20, 20)) # make a 20x20 ss
#     i = 0
#     while os.path.exists('tmp/wpt%s.png' % i):
#         i += 1
#     ss.save('tmp/wpt%s.png' %i)

# def run():
#     x = []
#     while True:
#         try:
#             if msvcrt.kbhit():
#                 key = msvcrt.getch()
#                 if key == b'\xe0':
#                     ss_wpt()
#                 x.append(key)
#                 print(x)
#         except KeyboardInterrupt:
#             break

# run()
