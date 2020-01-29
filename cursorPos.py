import pyautogui as pag
import time
import os


def get_mouse_position():
    x, y = pag.position()
    positionStr = 'X: {}   Y: {}'.format(x, y)
    # positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    print(positionStr)


while True:
    os.system('clear')
    get_mouse_position()
    time.sleep(0.5)
