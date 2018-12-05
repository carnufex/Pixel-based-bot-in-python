import imageSearch as imgS

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
                        click_image(wptImg, (wpt[0]+miniMapPos[0], wpt[1]+miniMapPos[1]), "left", 1)
                        time.sleep(10)
                    else:
                        print("wpt not found")
            except KeyboardInterrupt:
                break
    else:
        print("minimap not found")


main()