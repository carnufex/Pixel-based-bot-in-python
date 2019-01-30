import imageSearch as imgS
import time
import msvcrt
import pyautogui
import os

waypoints = ["assets/checkmark-wpt.png", "assets/questionmark-wpt.png", "assets/exclimationmark-wpt.png", "assets/star-wpt.png", "assets/cross-wpt.png"]
#waypoints = ["checkmark-wpt.png", "questionmark-wpt.png", "exclimationmark-wpt.png", "cross-wpt.png"]
def initMinimap():
    minimapStart = imgS.imagesearch("assets/minimap.png", 0.8)
    minimapEnd = imgS.imagesearch("assets/minimap-end.png", 0.8)
    if (minimapStart[0] != -1) and (minimapEnd[0] != -1):
        return (minimapStart[0], minimapStart[1], minimapEnd[0], minimapEnd[1])
    else:
        return (-1,-1,-1,-1)

def main():
    miniMapPos = initMinimap()
    if miniMapPos[0] is not -1:
        # pyautogui.moveTo(minimapEnd[0], minimapEnd[1])
        while True:
            try:
                for wptImg in waypoints:
                    # print("minimapPos", miniMapPos[0], miniMapPos[1], miniMapPos[2], miniMapPos[3])
                    wpt = imgS.imagesearcharea(wptImg, miniMapPos[0], miniMapPos[1], miniMapPos[2], miniMapPos[3], 0.7)
                    if wpt[0] is not -1:
                        imgS.click_image(wptImg, (wpt[0]+miniMapPos[0], wpt[1]+miniMapPos[1]), "left", 0)
                        time.sleep(15)
                    else:
                        print("wpt not found")
            except KeyboardInterrupt:
                break
    else:
        print("minimap not found")


#main()

def ss_wpt():
    x,y = pyautogui.position()
    ss = imgS.region_grabber((x, y, 20, 20)) # make a 20x20 ss
    i = 0
    while os.path.exists('tmp/wpt%s.png' % i):
        i += 1
    ss.save('tmp/wpt%s.png' %i)

def run():
    x = []
    while True:
        try:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0':
                    ss_wpt()
                x.append(key)
                print(x)
        except KeyboardInterrupt:
            break

run()
