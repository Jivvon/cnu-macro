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
import multiprocessing
import pyautogui as pag


def getNumber(pos):
    recogtest = Recognition(pos[0], pos[1], pos[0] + pos[2], pos[1] + pos[3])
    result = recogtest.ExtractNumber()
    while (len(result) == 4 and 0 <= int(result) <= 9999):
        time.sleep(0.2)
        result = recogtest.ExtractNumber()
    print(result)
    return result


def readFile():
    ret = []
    with open('positions.txt', 'r') as f:
        for line in f.readlines():
            if(line[0].isdigit()):
                ret.append(list(map(int, line[:-1].split(' '))))

    def chunker(seq, size):
        return list(seq[pos:pos + size] for pos in range(0, len(seq), size))

    return chunker(ret, 4)


def click(x, y):
    pag.moveTo(x=x, y=y, duration=0.0)
    pag.mouseDown()
    pag.mouseUp()


def dbclick(arr):
    # print("double click ")
    # print(arr)
    click(arr[0], arr[1])
    click(arr[0], arr[1])


def init(param):
    # 화면 setting #
    # time.sleep(1)
    window = param[0]
    pos = param[1:]
    dbclick(pos[0][window])  # 수강신청 들어가기
    time.sleep(3)
    dbclick(pos[1][window])  # 안내문 ok
    time.sleep(1)
    dbclick(pos[2][window])  # 왼쪽 창 접기
    time.sleep(1)


def initWindow(param):
    multiprocessing.set_start_method('spawn')
    arr = list([i] + param[:3] for i in range(4))
    with multiprocessing.Pool(processes=8) as pool:
        pool.map(init, arr)


def macro(window):
    window = param[0]
    pos = param[1:]
    num = getNumber(pos[1][window])
    dbclick(pos[0][window])  # 확정하기
    keyboard.Type(num + '\n')


def run(param):
    multiprocessing.set_start_method('spawn')
    arr = list([i] + param[6:] for i in range(4))
    with multiprocessing.Pool(processes=8) as pool:
        pool.map(macro, arr)


http = urllib3.PoolManager()
url = 'http://cnuis.cnu.ac.kr'
response = http.request('GET', url)
date = response.headers['Date']
date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')

timegap = 0.2

###
# USER SETTING #
(h, m, s) = (4, 3, 30)
gametime = date.replace(minute=00, second=00)
print(gametime)
###


# 1초 동안 약 0.2 딜레이
if __name__ == '__main__':
    pos = readFile()
    initWindow(pos)
while True:
    os.system('clear')
    response = http.request('GET', url)
    date = response.headers['Date']
    date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
    flag = gametime - date < datetime.timedelta(seconds=2)  # 1초 전 true
    print(date)
    if flag:
        time.sleep(0.4)  # 0.4초 뒤에 실행
        break
    time.sleep(timegap)
run(pos)
