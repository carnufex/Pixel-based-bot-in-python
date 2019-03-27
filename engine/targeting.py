'''targeting enginge'''
import time
import pyautogui
from lib import imageSearch as imgS
from lib import utilities, sendInput

#check amount of monsters - by checking for empty spot?
def target(gui):
    '''look for targets'''
    battlelist_coords = utilities.find_battlelist()
    targeting = is_targeting(battlelist_coords)
    if battlelist_coords[0] is not -1 and not targeting:
        targets = has_targets(battlelist_coords)
        if targets:
            #not empty battlelist
            attack(gui.title)




def attack(title):
    '''attack monster'''
    sendInput.send_key("space", title=title)
    time.sleep(1)

def main(gui, minimum):
    '''runs targeting'''
    while True:
        target(gui.title, minimum)
        time.sleep(4)

def is_targeting(battlelist_coords):
    # utilities.dev_find_color(battlelist_coords[0][0], battlelist_coords[0][1], battlelist_coords[0][0]+1, battlelist_coords[1][1])
    target_color = [255, 0, 0]
    killing = utilities.find_pixel_color(target_color, target_color, 0, battlelist_coords[0][0], battlelist_coords[0][1], battlelist_coords[0][0]+1, battlelist_coords[1][1])
    # print(target)
    if killing[0] is not -1:
        return True
    return False

def has_targets(battlelist_coords):
    '''checks battlelist for monsters'''
    no_monster = "assets/battlelist/empty.png"
    monster = imgS.imagesearcharea(no_monster, battlelist_coords[0][0], battlelist_coords[0][1], \
            battlelist_coords[1][0], battlelist_coords[1][1], precision=0.8)
    if monster[1] is -1 or monster[1] > 40:
        return True
    return False