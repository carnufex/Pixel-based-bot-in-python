from pynput import keyboard
import imageSearch as imgS
import time
import pyautogui
import os
import gfb


def ss_wpt(size):
    size = size / 2
    x,y = pyautogui.position()
    ss = imgS.region_grabber((x-size, y-size, x+size, y+size)) # make the ss centered around mouse
    i = 0
    while os.path.exists('tmp/wpt%s.png' % i):
        i += 1
    ss.save('tmp/wpt%s.png' %i)

# The key combination to check
ScreenShot_HK = [
    {keyboard.Key.shift, keyboard.KeyCode(char='a')},
    {keyboard.Key.shift, keyboard.KeyCode(char='A')}
]


# The currently active modifiers
current = set()
# Listener as global to easily stop it.
listener = None
gui = None
config = None

def on_press_helper(key):
    for hk in config.items('SAVED_VARS'):
        pressed = str(key).replace("Key.", "")
        hotkey = hk[1].replace("'", "")
        if pressed == hotkey:
            button = gui.hotkey_checkButton_dict[hk[0]]
            button.invoke()


def on_press(key):
    on_press_helper(key)

    if any([key in COMBO for COMBO in ScreenShot_HK]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in ScreenShot_HK):
            print ("saved screenshot")
            ss_wpt(500)


def on_release(key):
    if any([key in COMBO for COMBO in ScreenShot_HK]):
        current.remove(key)

def stop():
    print("Stopping hk listener")
    listener.stop()


def start(gui_class, config_parser):
    global listener
    global gui
    global config
    gui = gui_class
    config = config_parser

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()
