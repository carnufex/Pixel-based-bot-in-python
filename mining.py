import imageSearch as imgS
import time
import pyautogui

mineList = ["assets/mines/gold.png", "assets/mines/coal.png"]
# function to get the cords for 1sqm around character in every direction.
def searchArea():
    res = pyautogui.size()
    xStart = int(res[0] / 2.4)
    yStart = int(res[1] / 2.48)
    xEnd = int(res[0] / 1.80)
    yEnd = int(res[1] / 1.67)
    return (xStart, yStart, xEnd, yEnd)

'''

Searches for ores in proximity to the character

input :
cordsTuple : tuple of (top left x value, top left y value, bottom right x value, bottom right y value)
mineTypes : list of name(s) of the mines you want to look for, names must match with images in assets/mines.

returns : coordinates of found mine
'''
def lookForOres(coordsTuple, mineTypes):
    mineTypes = list(map(lambda oldString: "assets/mines/" + oldString + ".png", mineTypes))
    ores = set(mineList).intersection(mineTypes) # find only the ores we are interested in.
    orePos, ore = imgS.imagesearch_array_region_loop(ores, 5, coordsTuple[0], coordsTuple[1], coordsTuple[2], coordsTuple[3], 0.8)
    print(orePos, ore)
    return (orePos[0] + coordsTuple[0], orePos[1] + coordsTuple[1]), ore

def gatherOre(image, coords, action):
    imgS.click_image(image, coords, action, 0)
    time.sleep(1)
    imgS.click_image(image, coords, action, 0)

def main():
    # init search area
    area = searchArea()
    while True:
        try:
            oreCoords, ore = lookForOres(area, ["coal"])
            print("found ore at: ", oreCoords)
            gatherOre(ore, oreCoords, "right")
        except KeyboardInterrupt:
            break


main()
