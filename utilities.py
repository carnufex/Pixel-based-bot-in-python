import imageSearch as imgS
import pyautogui
import win32api, win32con, win32gui
from ctypes import windll
import time

def has_cd(img, x, y, im=None):
    img = 'assets/cds/{}.png'.format(img)
    no_cd = imgS.imagesearcharea(img, x, y, x+50, y+50, 0.7, im)
    if no_cd[0] is not -1:
        #it has no cd, return false
        return False
    else:
        return True


# Code to check if left or right mouse buttons were pressed

def detect_mouse_click(arg):
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

    while True:
        a = win32api.GetKeyState(0x01)

        if a != state_left:  # Button state changed
            state_left = a

            if a < 0:
                #print('Left Button Pressed')
                coords = pyautogui.position()
                return coords

    time.sleep(0.001)


def string2tuple(old_string):
    new_tuple = tuple(int(x) for x in old_string[1:-1].split(','))
    return new_tuple



def key2hex(key):
    if key == 'F1' or key == 'f1':
        key = hex(ord(';'))
    elif key == 'F2' or key == 'f2':
        key = hex(ord('<'))
    elif key == 'F3' or key == 'f3':
        key = hex(ord('='))
    elif key == 'F4' or key == 'f4':
        key = hex(ord('>'))
    elif key == 'F5' or key == 'f5':
        key = hex(ord('?'))
    elif key == 'F6' or key == 'f6':
        key = hex(ord('@'))
    elif key == 'F7' or key == 'f7':
        key = hex(ord('A'))
    elif key == 'F8' or key == 'f8':
        key = hex(ord('B'))
    elif key == 'F9' or key == 'f9':
        key = hex(ord('C'))
    elif key == 'F10' or key == 'f10':
        key = hex(ord('D'))
    elif key == 'F11' or key == 'f11':
        key = hex(122)
    elif key == 'F12' or key == 'f12':
        key = hex(123)
    elif key == 'Del' or key == 'DEL' or key == 'del':
        key = hex(ord('S'))
    elif key == 'Ins' or key == 'INS' or key == 'ins':
        key = hex(ord('R'))
    elif key == 'Home' or key == 'HOME' or key == 'home':
        key = hex(ord('G'))
    elif key == 'End' or key == 'END' or key == 'end':
        key = hex(ord('O'))
    elif key == 'PgUp' or key == 'PGUP' or key == 'pgup' or key == 'Pgup':
        key = hex(ord('I'))
    elif key == 'PgDn' or key == 'PGDN' or key == 'pgdn' or key == 'Pgdn':
        key = hex(ord('Q'))

    hex_int = int(key, 16)
    return hex_int



# def init():
#     appname = "Tibia"
#     window = win32gui.FindWindow(None, appname)
#     try:
#         win32gui.SetForegroundWindow(window)
#     except:
#         pass
