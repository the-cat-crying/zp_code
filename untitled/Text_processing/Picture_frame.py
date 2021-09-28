import cv2 as cv
import numpy as np


h = cv.imread('/home/zhoup/test/images/bird3.jpg')
# h = cv.resize(o, (0, 0), fx=0.3, fy=0.3, interpolation=cv.INTER_NEAREST)
gray = cv.cvtColor(h, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
rect = cv.minAreaRect(contours[0])
print('返回值 rect:\n', rect)
points = cv.boxPoints(rect)
print('\n转换后 points: \n', points)
point = np.int0(points)
gray = cv.drawContours(h, [point], 0, (255, 255, 255), 2)
cv.imshow('hh', h)
cv.waitKey()
cv.destroyAllWindows()
