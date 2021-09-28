import cv2 as cv


# 去噪点
o = cv.imread('/home/zhoup/test/images/bird4.jpg')
h = cv.resize(o, (0, 0), fx=0.2, fy=0.2, interpolation=cv.INTER_NEAREST)
g = cv.GaussianBlur(h, (9, 9), 0, 0)
b = cv.bilateralFilter(h, 20, sigmaColor=200, sigmaSpace=100)
cv.imshow('hh', h)
cv.imshow('gg', g)
cv.imshow('bb', b)
cv.waitKey()
cv.destroyAllWindows()
