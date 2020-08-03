import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageGrab


class Recognition:
    def __init__(self, positions, img_path):
        self.positions = positions
        self.path = img_path

    def grab_image(self):
        img = ImageGrab.grab(bbox=self.positions)
        img.save(self.path)

    def ocr(self):
        src_path = "thres.png"
        img = cv2.imread(self.path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply dilation and erosion to remove some noise
        kernel = np.ones((1,1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        # Write image after removed noise
        ###### cv2.imwrite("removed_noise.png", img)
        #  Apply threshold to get image with only black and white
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

        # 이미지 가공 후 총 결과
        cv2.imwrite(src_path, img)
        # OCR . config='digits' 제외해도 가능
        result = pytesseract.image_to_string(Image.open(src_path),lang='eng', config='digits')
        return result.strip()


if __name__ == '__main__':
    img_path = 'screenshot.png'
    recognition = Recognition((1025, 280, 1028+74, 288+27), img_path)
    recognition.grab_image()
    recognition.ocr()
