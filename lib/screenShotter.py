import cv2
import numpy as np
import pyautogui
import random
import time
import win32gui
import win32ui
from ctypes import windll
from PIL import Image

'''

grabs a region of your game client.

output : a PIL image of the area selected.

'''

def run(gui):
    gui.currentImage = region_grabber()



def region_grabber():
    start = time.time()
    hwnd = win32gui.FindWindow(None, 'Windowed Projector (Preview)')

    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = int(right - left)
    h = int(bot - top)

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    # print(result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer('RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        #im.save("test.png")
        end = time.time()
        #print("TIME: ", end - start)
        return im
    else:
        print("Something went shit in region_grabber()")
