# Preprocesses on number plate image and reads

import cv2
import numpy as np
import pytesseract
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
from PIL import Image
import imutils
import os
import sys


def main():
    orig = cv2.imread("img1.PNG")
    prep_img = prep(orig)
    read(prep_img)


def read(thresh):
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, thresh)
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    print(text)


def prep(orig):
    # perform all the preprocessing here
    '''
    resize
    deskew
    grayscale+blur
    threshold
    erode/dilate
    perspective transform- not reqd for current set of images. However, in real life applications, useful. to implement it, first find plate contour, make sure only 4 corner points are obtained from cv2.approxPolyDP, then pass it to imutils.four_point_transform()

    '''
    orig = cv2.resize(orig, (1024, 256))
    thresh = Grayscale_Threshold(orig)  # for the original image


# To deskew the image
    # coordinates stored in columns
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]  # returns rotated rectangle

    if angle < -45:
        angle = -(90 + angle)
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle

    (h, w) = orig.shape[:2]

    center = (w // 2, h // 2)  # rounded to the nearest whole number
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    orig = cv2.warpAffine(orig, M, (w, h),
                          flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)  # text rotated by the appropriate angle
# Deskewing complete here

# erosion and dilation
    orig = cv2.erode(orig, (10, 10))
    thresh = Grayscale_Threshold(orig)  # for the deskewed image


# The following lines are for perspective transformation, which was not required for us-----------------------------
# contours found and drawn
    # contours, _ = cv2.findContours(
    #     thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # contours drawn correctly, capture contour with largest/secondlargest perimeter

    # cv2.drawContours(orig, contours, -1, (255, 255, 0), 3)

    # peri = []
    # for c in contours:
    #     peri.append(cv2.arcLength(c, True))

    # maxpos = peri.index(max(peri))
    # peri[maxpos] = 0
    # # this stores the second largest contour, the number plate boundary
    # maxpos2 = peri.index(max(peri))

    # perimeter = peri[maxpos2]
    # epsilon = 0.01*perimeter
    # approx = cv2.approxPolyDP(contours[maxpos2], epsilon, True)

    # cv2.drawContours(orig, approx, -1, (0, 255, 0),
    #                  10)  # draws the corner points
    # cv2.drawContours(orig, contours, maxpos, (0, 0, 100), 3)

    # # Perspective Transformation

    # # Perspective_img = four_point_transform(orig, approx.reshape(4, 2))  # only rectangle can be passed
    # # Perspective_img_gray = four_point_transform(gray_not, approx.reshape(4, 2))
# ---------------------------------------------------------------------------------------------------
    cv2.imshow('1', orig)
    cv2.imshow('2', thresh)
    cv2.waitKey(0)

    return thresh


def Grayscale_Threshold(img):

    # greyscale and blurring
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_not = cv2.bitwise_not(gray)  # inverts each color


# threshold
    thresh = cv2.threshold(gray_not, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    thresh = clear_border(thresh)

    return thresh


if __name__ == "__main__":
    main()
