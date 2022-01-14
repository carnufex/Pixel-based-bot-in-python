from pynput import keyboard
from lib import imageSearch as imgS
import time
import pyautogui
import os


def ss_wpt(size):
    size = size / 2
    x,y = pyautogui.position()
    ss = imgS.region_grabber((x - size, y - size, x + size, y + size)) # make the ss centered around mouse
    i = 0
    while os.path.exists('tmp/wpt%s.png' % i):
        i += 1
    ss.save('tmp/wpt%s.png' % i)

# The key combination to check
ScreenShot_HK = [{keyboard.Key.shift, keyboard.KeyCode(char='a')},
    {keyboard.Key.shift, keyboard.KeyCode(char='A')}]


# The currently active modifiers
current = set()
# Listener as global to easily stop it.
listener = None
gui = None

def on_press_helper(key):
    for hk in gui.config.items('ENGINE_HOTKEYS'):
        pressed = str(key).replace("Key.", "")
        hotkey = hk[1].replace("'", "")
        if pressed == hotkey:
            button = gui.hotkey_checkButton_dict[hk[0]]
            button.invoke()
            break


def on_press(key):
    on_press_helper(key)

    if any([key in COMBO for COMBO in ScreenShot_HK]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in ScreenShot_HK):
            print("saved screenshot")
            ss_wpt(500)


def on_release(key):
    if any([key in COMBO for COMBO in ScreenShot_HK]):
        current.remove(key)

def stop():
    print("Stopping hk listener")
    listener.stop()


def start(gui_class):
    global listener
    global gui
    gui = gui_class
    config = gui.config

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()
