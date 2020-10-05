# cnu-macro

충남대학교 수강신청 매크로

<hr>

## 실행 환경

```
mac 13'
1440 x 900
safari 4 split windows (top-left, top-right, bottom-left, bottom-right)
Python 3.6.9 :: Anaconda, Inc.
```

<hr>

## keyboard.py

키보드 입력 지원

<hr>

## cursorPos.py

마우스 좌표 출력

<hr>

## recognition.py

OCR을 통한 매크로 방지 숫자 인식

<hr>

## macro.py

메인 매크로 실행파일

USER SETTING : 수강신청 시작시간 설정

충남대학교 서버시간 (http://cnuis.cnu.ac.kr) 을 가져와 0.6초 전 실행 ( 서버시간을 가져오는 시간과 매크로를 실행하여 서버로 넘어가는 시간이 있다. )

각 버튼의 위치는 positions.txt에서 가져와 사용

수강신청 시작할 때에는 사용자가 많이 몰려 바로 매크로 방지 숫자가 나타나지 않으므로 정확한 숫자를 읽을 때까지 반복

<hr>

## positions.txt

각 버튼들의 위치 ( 실행 환경 기준 )

각 line의 시작이 숫자가 아니면 macro.py에서 무시함

TODO : #7 확정하기 버튼 4 개 추가 예정
