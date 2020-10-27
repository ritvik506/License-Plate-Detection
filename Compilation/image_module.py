import cv2
import imutils
import numpy as np
from imutils.perspective import four_point_transform
import sys


def image_module(img):

    img = cv2.resize(img, (600, 400))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)

    edged = cv2.Canny(gray, 30, 200)
    contours = cv2.findContours(
        edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in contours:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            screenCnt = screenCnt.reshape(4, 2)
            idx = contours.index(c)
            bird_eye = four_point_transform(img, screenCnt)
            # cv2.imshow('trial', bird_eye)
            # cv2.waitKey(0)
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

    cv2.imshow('Plate-Cropped', bird_eye)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return bird_eye
