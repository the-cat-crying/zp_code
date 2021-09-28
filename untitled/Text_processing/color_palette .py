import cv2 as cv
import numpy as np

img = np.zeros((100, 700, 3), np.uint8)


def chang_color(x):
    r = cv.getTrackbarPos('R', 'image')
    g = cv.getTrackbarPos('G', 'image')
    b = cv.getTrackbarPos('B', 'image')
    img[:] = [b, g, r]


cv.namedWindow('image')
cv.createTrackbar('R', 'image', 0, 255, chang_color)
cv.createTrackbar('G', 'image', 0, 255, chang_color)
cv.createTrackbar('B', 'image', 0, 255, chang_color)


while True:
    cv.imshow('image', img)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
k
cv.destroyAllWindows()
