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
import multiprocessing as mp
import pyautogui as pag

windows = 1


def getNumber(pos):
    # print('pos : ', pos)
    time.sleep(0.5)
    recogtest = Recognition(pos[0], pos[1], pos[2], pos[3])
    result = recogtest.ExtractNumber()
    if len(str(result)) == 3 or len(str(result)) == 2:
        return 0000
    i = 1
    try:
        while not (len(result) == 4 and 0 <= int(result) <= 9999):
            time.sleep(0.3)
            result = recogtest.ExtractNumber()
            i += 1
            if i > 1 or len(str(result)) == 3 or len(str(result)) == 2:
                result = 0000
                time.sleep(1)
                break
    except Exception:
        result = 0000
    return result


def readFile():
    ret = []
    with open('positions_{}.txt'.format(windows), 'r') as f:
        for line in f.readlines():
            if(line[0].isdigit()):
                ret.append(list(map(int, line[:-1].split(' '))))

    def chunker(seq, size):
        return list(seq[pos:pos + size] for pos in range(0, len(seq), size))

    # return ret
    return chunker(ret, windows)


def click(x, y):
    pag.moveTo(x=x, y=y, duration=0.0)
    pag.mouseDown()
    pag.mouseUp()


def dbclick(arr):
    click(arr[0], arr[1])
    time.sleep(0.05)
    click(arr[0], arr[1])


def macro(param):
    dbclick(pos[0][0])  # 확정하기
    keyboard = Keyboard()
    num = getNumber(pos[1][0])
    print("num : ", num)
    keyboard.Type(str(num))
    keyboard.Type('\n')
    time.sleep(0.5)
    keyboard.Type('\n')


def run(param):
    try:
        mp.set_start_method('spawn')
    except RuntimeError:
        pass
    with mp.Pool(processes=1) as pool:
        pool.map(macro, param)


if __name__ == '__main__':
    pos = readFile()
    while True:
        macro(pos)
