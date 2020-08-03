from newrecognition import Recognition
import pyautogui as pag

pag.PAUSE = 0.4

data = {
    'rolldown' : (373,376),
    'rollclassname' : (373,512),
    'searchbar' : (680,376),
    'classname' : '기계학습',
    'submit' : (260,760)
}


# 과목명 검색
def init():
    pag.click(data['rolldown'])
    pag.click(data['rollclassname'])
    pag.click(data['searchbar'])
    pag.press('enter')

# 신청 버튼 누르기
def press_submit():
    pag.click(data['submit'])


# 매크로방지입력숫자 위치 찾기
def find_window():
    location = pag.locateOnScreen('window_top.png', grayscale=True, confidence=.95)
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
    pag.typewrite(number, interval=0.18)
    pag.sleep(0.2)
    pag.press('enter') # 저장
    pag.sleep(0.2)
    pag.press('enter') # 오류창 확인


if __name__ == '__main__':
    pag.click(30, 500) # 활성화
    # init() # 과목명 검색해서 제일 위에 노출되도록
    while True:
        press_submit() # 신청버튼 누르기
        location = find_window() # 매크로방지입력숫자 위치 찾기
        if not location:
            pag.press('enter') # 저장
            pag.typewrite('0000')
            pag.press('enter') # 저장
            continue
        recognition = Recognition(location, 'screenshot.png') # OCR
        recognition.grab_image() # 숫자 캡처하고
        number = recognition.ocr() # 숫자 읽어낸다
        print(number)
        save_number(number) # 숫자타이핑 하고 저장
        pag.sleep(1)

