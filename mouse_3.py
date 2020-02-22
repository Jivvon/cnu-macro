import urllib3
import cv2
import time
import os
import datetime
import re
import numpy as np
from recognition import Recognition
from pytesseract import *
from PIL import Image, ImageGrab
from keyboard import Keyboard
# from multiprocessing import Pool
import multiprocessing as mp
import pyautogui as pag


def click(x, y):
    pag.moveTo(x=x, y=y, duration=0.0)
    pag.mouseDown()
    pag.mouseUp()


def dbclick(arr):
    # print("double click ", arr)
    # print(arr)
    click(arr[0], arr[1])
    time.sleep(0.05)
    click(arr[0], arr[1])


def dbclick(x, y):
    click(x, y)
    time.sleep(0.05)
    click(x, y)


pos_x = [365, 827, 1213]
pos_y = [324, 324, 324]


def tt(param):
    mp.set_start_method('spawn')
    arr = list(pos_x)
    with mp.Pool(processes=2) as pool:
        pool.map(init, arr)
    time.sleep(3)


if __name__ == '__main__':
    while True:
        for i in range(3):
            dbclick(pos_x[i], pos_y[i])
        time.sleep(0.1)
