import pyautogui
import time
import pyperclip
import os
import numpy as np
import json
import collections
from PIL import Image
import math
pyautogui.PAUSE = 0.1
time.sleep(2)

#Top Left of screen and size
#screen = (20,150,2776,1631)
screen = (20,120,1845,910)
#                1378,740
#screen = (20,150,1000,1000)

screenDivider = 1 # screen divider is used if Amidst has multiple pixels dedicated to the same area
command = "ctrl"

def main():
    print("SettingUp")

    print("Switch to Amidst")
    switchApp()

    print("Set Zoom")
    setZoom()

    print("Center")
    moveTo(0,0)

    print("Begin Loop")
    while True:
        print("newRandomSeed")
        newSeed()
        time.sleep(10)

        print("Getting Screenshots")
        screenshots = getScreenshots()

        print("GoToTerminal")
        switchApp()


        print("Finding portals")
        portals = findEndPortals(screenshots)
        biomeToSearchFor = 55 #55 is the magic Flower number
        print("Looking for biome: {0}".format(biomeName(biomeToSearchFor)))

        print("Generating Biome Array")
        biomeMap = convertToBiomeArray(screenshots)
        print("Generated Biome Array")
        
        
        found = False
        for i in portals:
            print(i)
            if biomeInSquareRadius (biomeToSearchFor, i["x"], i["z"], 10, biomeMap):
                print("FoundBiome")
                found = True
        
        print("Go Back to amidst")
        
        switchApp()
        time.sleep(0.5)
        if found:
            saveFullScreenshot()

        
        



def getScreenshots(region = screen):

    screenshots = dict()
    
    screenshots["empty"] = pyautogui.screenshot(region = region)

    pyautogui.hotkey(command, '3')
    screenshots["stronghold"] = pyautogui.screenshot('test.png',region = region)
    pyautogui.hotkey(command, '3')

    return screenshots

def convertToBiomeArray(screenshots):
    img=screenshots["empty"]
    arr = np.array(img)
    biomeArr = []
    for i in range(math.floor(len(arr)/screenDivider)):
        biomeArr.append([])
        for k in range(math.floor(len(arr[i*screenDivider])/screenDivider)):
            thingToAppend = colorProfile["colors"].index([arr[i*screenDivider][k*screenDivider][0], arr[i*screenDivider][k*screenDivider][1], arr[i*screenDivider][k*screenDivider][2]])
            biomeArr[i].append(thingToAppend)
    return biomeArr





def saveFullScreenshot():
    pyautogui.hotkey(command, '2','3', '4', '5', '7')


    seed = getSeed()
    foldername = 'Seed '+seed
    dir = outputFile(foldername)

    if not os.path.exists(dir):
        os.mkdir(dir)
    
    filename = 'image.png'     
    fle = outputFile(foldername,filename)
    pyautogui.screenshot(fle) # Full Screen Image for saving

    pyautogui.hotkey(command, '2','3', '4', '5', '7')



def findEndPortals(screenshots):
    img = screenshots["stronghold"]
    portals = pyautogui.locateAll(configFile("EndPortal.png"), img)
    portalCenters = []
    
    for i in portals:
        x = round(i.left + i.width/2)
        z = round(i.top + i.height/2)

        x = round (x/screenDivider)
        z = round (z/screenDivider)

        portalCenters.append({"x": x, "z": z})
    
    return portalCenters

def biomeInSquareRadius(biome, centerX, centerZ, radius, biomeMap):
    count = 0
    print("Biome map dim = [{0}][{1}]".format(len(biomeMap), len(biomeMap[0])))
    for i in range(centerX - radius, centerX + radius):

        for j in range(centerZ - radius, centerZ + radius):
            if j < len(biomeMap) and i < len(biomeMap[j]):
                if biomeMap[j][i] == biome:
                    count +=1
    return count

def biomeName(biome):
    return colorProfile["names"][biome]

def getProfile(filename):
    jsonFile = open(filename,'r')

    prof = json.load(jsonFile)
    jsonFile.close()
    returning = {"colors": [],"names": []}
    for biome in prof["colorMap"]:
        red = biome[1]['r']
        green = biome[1]['g']
        blue = biome[1]['b']
        biomeName = biome[0]
        #print("{0}: ({1},{2},{3})".format(biomeName,red,green,blue))
        returning["colors"].append([red,green,blue])
        returning["names"].append(biomeName)

    return returning




def getIdFromPositon(imgArr, x, y):
        return colorProfile["colors"].index([imgArr[x*screenDivider][y*screenDivider][0], imgArr[x*screenDivider][y*screenDivider][1], imgArr[x*screenDivider][y*screenDivider][2]])
'''
def getBiomeScreenshot(region=screen):
    img=pyautogui.screenshot(region=region)
    arr = np.array(img)
    biomeArr = []
    for i in range(math.floor(len(arr)/screenDivider)):
        biomeArr.append([])
        for k in range(math.floor(len(arr[i*screenDivider])/screenDivider)):
            thing = colorProfile["colors"].index([arr[i*screenDivider][k*screenDivider][0], arr[i*screenDivider][k*screenDivider][1], arr[i*screenDivider][k*screenDivider][2]])
            biomeArr[i].append(thing)
    return biomeArr
          



def OldScreenshots():
    height = 3104
    width = 5232
    seed = getSeed()
    foldername = 'Seed '+seed
    dir = outputFile(foldername)
    if not os.path.exists(dir):
        os.mkdir(dir)

    for x in range(1,2):
        for z in range(1,2):
            sWidth = str(x*height)
            sHeight = str(z*width)
            
            sX=str(x)
            sZ=str(z)
            pyautogui.hotkey('command', 'shift', 'c')
            pyautogui.typewrite(sWidth + ',' + sHeight+'\n')
            time.sleep(10)
            filename = sX + ', ' + sZ+'.png'
            
            fle = outputFile(foldername,filename)
            pyautogui.screenshot(fle,region=screen) # Screen set above.




    seed = getSeed()
    foldername = 'Seed '+seed
    dir = outputFile(foldername)
    if not os.path.exists(dir):
        os.mkdir(dir)

            filename = 'image.png'
            
            fle = outputFile(foldername,filename)
            pyautogui.screenshot(fle,region=screen) # Screen set above.



'''

def switchApp():
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt') 


# Folder Functions
def checkDir():
    path = os.path.join("Josh","temp")
    if os.path.exists(path):
        print(path + ' : exists')
        if os.path.isdir(path):
            print(path + ' : is a directory')

def configFile(*args, **kwargs):
    return os.path.join("config", *args, **kwargs)

def outputFile(*args, **kwargs):
    return os.path.join("output", *args, **kwargs)



def OldScreenshots():
    height = 3104
    width = 5232
    seed = getSeed()
    foldername = 'Seed '+seed
    dir = outputFile(foldername)
    if not os.path.exists(dir):
        os.mkdir(dir)

    for x in range(1,2):
        for z in range(1,2):
            sWidth = str(x*height)
            sHeight = str(z*width)
            
            sX=str(x)
            sZ=str(z)
            pyautogui.hotkey(command, 'shift', 'c')
            pyautogui.typewrite(sWidth + ',' + sHeight+'\n')
            time.sleep(10)
            filename = sX + ', ' + sZ+'.png'
            
            fle = outputFile(foldername,filename)
            pyautogui.screenshot(fle,region=screen) # Screen set above.


# Amidst Functions
def moveTo(x, z):
    pyautogui.hotkey(command, 'shift', 'c')
    pyautogui.typewrite("{0}, {1}\n".format(x, z))

def setZoom():
    if False:
        for i in range(30):
            pyautogui.hotkey(command, 'k')
        for i in range(20):
            pyautogui.hotkey(command, 'j')


def newSeed():
    pyautogui.hotkey(command, 'r')


def getSeed():
    pyautogui.hotkey(command, 'c')
    time.sleep(1)
    return pyperclip.paste()

# Helper functions. Should have own class but to lazy to figure out python classes
def ListDimensions(a):
    if not type(a) == list:
        return []
    return [len(a)] + ListDimensions(a[0])



def clamp (x, lower, upper):
    return max(lower, min(upper, x))


# Call main from the bottom so everything else is defined
if __name__ == "__main__":
    colorProfile = getProfile(configFile("biomeProfile.json"))
    main()
    #saveFullScreenshot()
