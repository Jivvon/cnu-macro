import cv2
import numpy as np
import pytesseract
import re
from PIL import Image, ImageGrab


class Recognition:
    def __init__(self, x, y, w, h):
        self.xx = x * 2
        self.yy = y * 2
        self.ww = w * 2
        self.hh = h * 2

    def cleanText(self, readData):
        text = re.sub(
            '[-=+,#/\?:^$.@*\"※~&%ㆍ!」』\\‘|\(\)\[\]\<\>`\'…》 ]', '', readData)
        # 양쪽(위,아래)줄바꿈 제거
        # text = text.strip('\n')
        # print('@@@@@@@@@@@@@@@')
        # print(text)
        # print('@@@@@@@@@@@@@@@')
        try:
            text = re.search('\d+', text).group
            print(text)
        # text = text.replace("\n", "")
        # text = text.replace(" ", "")
            return text
        except Exception:
            return text

    def ExtractNumber(self):
        img = np.array(ImageGrab.grab(
            bbox=(self.xx, self.yy, self.ww, self.hh)))
        cv2.imwrite('image1.jpg', img)
        copy_img = img.copy()
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray_img, 245, 250)
        # _, contours, hierarchy = cv2.findContours(
        #     canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts, contours, hierarchy = cv2.findContours(
            canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # cnt = contours[0]
        # rect = cv2.minAreaRect(cnt)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        # contourimg = cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
        # cv2.imwrite('image1_c.jpg', contourimg)

        box1 = []
        f_count = 0
        select = 0
        plate_width = 0

        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            rect_area = w*h  # area size
            aspect_ratio = float(w)/h  # ratio = width/height

            # if (aspect_ratio >= 0.3)and(aspect_ratio <= 0.85)and(rect_area >= 380)and(rect_area <= 1200)and(h >= 35):
            if (aspect_ratio >= 0.3)and(aspect_ratio <= 0.85)and(rect_area >= 380)and(rect_area <= 1500)and(h >= 35):
                cv2.rectangle(canny, (x, y), (x+w, y+h), (0, 255, 0), 1)
                box1.append(cv2.boundingRect(cnt))

        cv2.imwrite('image2.jpg', canny)

        # 중복 제거
        box1 = list(set(box1))

        for i in range(len(box1)):  # Buble Sort on python
            for j in range(len(box1)-(i+1)):
                # x1 좌표 오름차순
                if box1[j][0] > box1[j+1][0]:
                    # 넓이 오름차순
                    # if box1[j][2]*box1[j][3]<box1[j+1][2]*box1[j+1][3]:
                    temp = box1[j]
                    box1[j] = box1[j+1]
                    box1[j+1] = temp

        print(box1)

        plate_x1 = 9999
        plate_x2 = 0
        plate_y1 = 9999
        plate_y2 = 0
        margin = 10

       # to find number plate measureing length between rectangles
        for m in range(len(box1)):
            # boax[m] = (x, y, w, h)
            # print(len(box1), 'box1[m] : ', box1[m])
            count = 0
            if plate_x1 > box1[m][0]:
                plate_x1 = box1[m][0]
            if plate_x2 < box1[m][0] + box1[m][2]:
                plate_x2 = box1[m][0] + box1[m][2]
            if plate_y1 > box1[m][1]:
                plate_y1 = box1[m][1]
            if plate_y2 < box1[m][1] + box1[m][3]:
                plate_y2 = box1[m][1] + box1[m][3]

            # print('good', m + 1, (len(box1) - 1))
            # for n in range(m + 1, (len(box1) - 1)):
            #     print('check', n, m)
            #     delta_x = abs(box1[n+1][0]-box1[m][0])
            #     if delta_x > 30:
            #         break
            #     delta_y = abs(box1[n+1][1]-box1[m][1])
            #     if delta_y > 30:
            #         break
            #     if delta_x == 0:
            #         delta_x = 1
            #     if delta_y == 0:
            #         delta_y = 1
            #     gradient = float(delta_y) / float(delta_x)
            #     if gradient < 0.1:
            #         count = count+1
            # # measure number plate size
            # if count > f_count:
            #     select = m
            #     f_count = count
            #     plate_width = delta_x

        print('plate pos : ', plate_x1, plate_x2, plate_y1, plate_y2)
        if plate_x1 == 9999 or plate_x2 == 0 or plate_y1 == 9999 or plate_y2 == 0:
            return 0
        number_plate = copy_img[plate_y1 - margin:plate_y2 +
                                margin, plate_x1 - margin:plate_x2+margin]
        # number_plate = copy_img[plate_x1 - margin:plate_x2 +
        #                         margin, plate_y1 - margin:plate_y2+margin]
        # cv2.imwrite('image3.jpg', number_plate)
        try:
            resize_plate = cv2.resize(
                number_plate, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
            # number_plate, None, fx=1.8, fy=1.8, interpolation=cv2.INTER_CUBIC+cv2.INTER_LINEAR)
        except Exception as e:
            resize_plate = number_plate
        plate_gray = cv2.cvtColor(resize_plate, cv2.COLOR_BGR2GRAY)
        ret, th_plate = cv2.threshold(plate_gray, 190, 255, cv2.THRESH_BINARY)
        # cv2.imwrite('image4.jpg', th_plate)

        kernel = np.ones((3, 3), np.uint8)
        er_plate = cv2.erode(th_plate, kernel, iterations=1)
        er_invplate = er_plate
        # cv2.imwrite('image5.jpg', er_invplate)
        result = pytesseract.image_to_string(er_invplate, lang='eng')
        self.cleanText(result)
        print('result : ', result)
        return result
        # return (result.replace(" ", ""))


# recogtest = Recognition()
# result = recogtest.ExtractNumber()
# print(result)
