'''clicks in a square around the character to grab some loot'''
from lib import sendInput, utilities
import pyautogui
import time

def loot(gui):
    '''finds character position and sqm size'''
    start = utilities.string2tuple(gui.config.get('GAMEWINDOW', 'game_start_coords'))
    end = utilities.string2tuple(gui.config.get('GAMEWINDOW', 'game_end_coords'))
    # screen is 15x11 sqms 
    sqm_width = (end[0]-start[0])/15
    sqm_height = (end[1]-start[1])/11
    left_x = start[0] + sqm_width * 6.5
    top_y = start[1] + sqm_height * 4.5
    click_loot(left_x, top_y, sqm_width, sqm_height, gui.title)



# click every sqm around the character?
def click_loot(left_x, top_y, sqm_width, sqm_height, title):
    '''clicks in a 3x3 grid around the char'''
    print("looting...")
    for x in range(3):
        loot_x = left_x + x*sqm_width
        for y in range(3):
            loot_y = top_y + y*sqm_height
            # pyautogui.moveTo(loot_x, loot_y)
            sendInput.send_click(loot_x, loot_y, title, 'right')
            time.sleep(0.1)

