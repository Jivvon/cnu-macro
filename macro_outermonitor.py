# newmacro.py backup
from newrecognition import Recognition
import pyautogui as pag

pag.PAUSE = 0.2


"""
user 환경 : Macos, Chrome, Flash Accept 
"""

data = {
    "rolldown": (373, 376),
    "rollclassname": (373, 512),
    "searchbar": (680, 376),
    "classname": "기계학습",
    "submit": (260, 756),
    "center": (640, 805),
}

search = {
    "search": (983, 376),
    "submit1": (264, 760),
    "students": (1140, 749, 1174, 767),
}

# 과목명 검색
def init():
    pag.click(data["rolldown"])
    pag.click(data["rollclassname"])
    pag.click(data["searchbar"])
    pag.press("enter")


# 신청 버튼 누르기
def press_submit():
    print("submit")
    pag.click(data["submit"])


# 매크로방지입력숫자 위치 찾기
def find_window():
    location = pag.locateOnScreen("window_top.png", grayscale=True, confidence=0.95)
    # location = pag.locateOnScreen('window_left.png', grayscale=True, confidence=.95)
    # pag.screenshot('find_window.png',region=location)
    print(location)
    try:
        window_x, window_y, _, _ = location
        x1 = window_x + 133
        y1 = window_y + 71 - 25
        x2 = x1 + 77
        y2 = y1 + 35
        return (x1, y1, x2, y2)
    except Exception:
        return None


def save_number(number):
    pag.typewrite(number, interval=0.05)
    pag.press("enter")  # 저장
    pag.sleep(0.1)
    pag.press("enter")  # 오류창 확인


def pass_error():
    pag.click(data["center"])
    pag.click(data["center"])
    pag.click(data["center"])


def pass_number():
    pag.press("enter")  # 저장
    pag.typewrite("0000")
    pag.press("enter")  # 저장


def run():
    count = 0
    prevNumber = ""
    prevFlag = False
    for _ in range(10):
    # while True:
        if count > 1:
            pass_error()
            count = 0
        press_submit()  # 신청버튼 누르기
        pag.sleep(0.2)
        location = find_window()  # 매크로방지입력숫자 위치 찾기
        if not location:
            pag.sleep(0.2)
            location = find_window()
        if not location:
            count += 1
            pass_number()
            continue
        recognition = Recognition(location, "screenshot.png")  # OCR
        recognition.grab_image()  # 숫자 캡처하고
        number = recognition.ocr()  # 숫자 읽어낸다
        print(prevNumber, number)
        if prevNumber == number:
            if prevFlag:
                pass_error()
                prevFlag = False
                continue
            prevFlag = True
        save_number(number)  # 숫자타이핑 하고 저장
        prevNumber = number
        pag.sleep(0.2)
    pass_error()


if __name__ == "__main__":
    pag.click(352, 140)  # 활성화
    while True:
        recognition = Recognition(search["students"], "screenshot.png")  # OCR
        recognition.grab_image()  # 숫자 캡처하고
        number = recognition.ocr()  # 숫자 읽어낸다
        print(number)
        try:
            if int(number) < 81:
                run()
            else:
                pag.press("enter")
                pag.click(search["search"])
                pag.sleep(0.4)
        except:
            print("!ERROR")
            run()
            pag.click(search["search"])
            pag.press("enter")
            pag.sleep(0.5)

