import imageSearch as imgS
import pyautogui

def has_cd(img, im=None):
    resolution = pyautogui.size()
    no_cd = imgS.imagesearcharea(img, 0, resolution[1]/2, resolution[0], resolution[1], 0.7, im)
    if no_cd[0] is not -1:
        #it has no cd, return false
        return False
    else:
        return True
