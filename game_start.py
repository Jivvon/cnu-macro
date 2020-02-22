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

pos = [[45, 565], [767, 565]]  # 왼쪽창 1번, 오른쪽창 1번


def click(x, y):
    pag.moveTo(x=x, y=y, duration=0.0)
    pag.mouseDown()
    pag.mouseUp()


def dbclick(arr):
    print("dbclick !!")
    click(arr[0], arr[1])
    # time.sleep(0.02)
    click(arr[0], arr[1])


def macro(param):  # param : [x, y]
    dbclick(param)  # 확정하기


def run():
    try:
        mp.set_start_method('spawn')
    except RuntimeError:
        pass
    with mp.Pool(processes=1) as pool:
        pool.map(macro, pos)


http = urllib3.PoolManager()
url = 'http://cnuis.cnu.ac.kr'
response = http.request('GET', url)
date = response.headers['Date']
date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')

timegap = 0.2

###
(h, m, s) = (0, 00, 0)
gametime = date.replace(hour=h, minute=m, second=s)
print(gametime)
###


# 1초 동안 약 0.2 딜레이
if __name__ == '__main__':
    while True:
        os.system('clear')
        response = http.request('GET', url)
        date = response.headers['Date']
        date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
        print(datetime.timedelta(seconds=2))
        flag = gametime - date > datetime.timedelta(seconds=2)  # 1초 전 true
        print(date)
        if flag:
            time.sleep(0)  # 0.2초 뒤에 실행
            break
        time.sleep(timegap)

    run()
