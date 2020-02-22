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

windows = 2


def getNumber(pos):
    print('pos : ', pos)
    time.sleep(0.5)
    recogtest = Recognition(pos[0], pos[1], pos[2], pos[3])
    result = recogtest.ExtractNumber()
    if len(str(result)) == 3 or len(str(result)) == 2:
        return 0000
    i = 0
    try:
        while not (len(result) == 4 and 0 <= int(result) <= 9999):
            time.sleep(0.3)
            result = recogtest.ExtractNumber()
            i += 1
            if i > 2 or len(str(result)) == 3 or len(str(result)) == 2:
                result = 0000
                time.sleep(2)
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

    return chunker(ret, windows)


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


def init(param):
    # 화면 setting #
    # time.sleep(1)
    window = param[0]
    pos = param[1:]
    dbclick(pos[0][window])  # 수강신청 들어가기
    time.sleep(5)
    dbclick(pos[1][window])  # 안내문 ok
    time.sleep(2)
    dbclick(pos[2][window])  # 왼쪽 창 접기
    time.sleep(3)


def initWindow(param):
    mp.set_start_method('spawn')
    arr = list([i] + param[:3] for i in range(windows))
    with mp.Pool(processes=1) as pool:
        pool.map(init, arr)
    time.sleep(3)


def macro(param):
    window = param[0]
    pos = param[1:]
    dbclick(pos[1][window])  # 확정하기
    # click(pos[1][window][0], pos[1][window][1])  # 확정하기
    keyboard = Keyboard()
    num = getNumber(pos[0][window])
    print(num)
    if num != 0:
        keyboard.Type(str(num)+'\n')
    time.sleep(1)
    keyboard.Type('\n')
    keyboard.Type('\n')


def run(param):
    try:
        mp.set_start_method('spawn')
    except RuntimeError:
        pass
    arr = list([i] + param[6:] for i in range(windows))
    # print(arr[1])
    # dbclick(arr[1])  # 확정하기
    with mp.Pool(processes=1) as pool:
        pool.map(macro, arr)


http = urllib3.PoolManager()
url = 'http://cnuis.cnu.ac.kr'
response = http.request('GET', url)
date = response.headers['Date']
date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')

timegap = 0.2

###
# USER SETTING #
(h, m, s) = (2, 30, 0)
gametime = date.replace(minute=m, second=s)
print(gametime)
###


# 1초 동안 약 0.2 딜레이
if __name__ == '__main__':
    pos = readFile()
    # initWindow(pos)
    # while True:
    #     os.system('clear')
    #     response = http.request('GET', url)
    #     date = response.headers['Date']
    #     date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
    #     flag = gametime - date < datetime.timedelta(seconds=2)  # 1초 전 true
    #     print(date)
    #     if flag:
    #         time.sleep(0.2)  # 0.2초 뒤에 실행
    #         break
    #     time.sleep(timegap)

    while True:
        run(pos)
