# A python program to find coordinates on screen
# May actually divide by 2 due to assumed bug in pyautogui
import pyautogui
import time
pyautogui.PAUSE = 0.1

x = y = 0
print(pyautogui.size())
new = old = veryOld = 0
while True:
    new = pyautogui.position()
    if new == old and old != veryOld:
        print(new)  # if the cursor has been in the same place for more than 1 second but less than 2 print the location
    veryOld = old
    old = new
    time.sleep(1)
