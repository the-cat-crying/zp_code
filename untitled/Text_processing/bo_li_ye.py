# -*- coding:utf-8 -*-
# 作者:周鹏
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

t = cv.imread('/home/zhoup/work/yolomark/img/20200506_work/images/000000.jpg', cv.IMREAD_GRAYSCALE)
# e = cv.adaptiveThreshold(x, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 5, 3)
t = cv.resize(t, (0, 0), fx=0.6, fy=0.6)
f = np.fft.fft2(t)
np_log = np.fft.fftshift(20 * np.log(np.abs(f)))

np_logs = np.fft.fftshift(f)
img = np.fft.ifft2(f)
iimg = np.abs(img)

b = 60
rows, cols = t.shape[0], t.shape[1]
crow, ccol = int(rows / 2), int(cols / 2)
np_logs[crow-b:crow+b, ccol-b:ccol+b] = 0
np_log[crow-b:crow+b, ccol-b:ccol+b] = 0

mmag = np.fft.ifftshift(np_logs)
imgs = np.fft.ifft2(mmag)
imgss = np.abs(imgs)

plt.subplot(221)
plt.imshow(t, cmap='gray')
plt.title('gg')
plt.axis('off')

plt.subplot(222)
plt.imshow(np_log, cmap='gray')
plt.title('hh')
plt.axis('off')

plt.subplot(223)
plt.imshow(iimg, cmap='gray')
plt.title('tt')
plt.axis('off')

plt.subplot(224)
plt.imshow(imgss, cmap='gray')
plt.title('ii')
plt.axis('off')

plt.show()
# cv.waitKey()
# cv.destroyAllWindows()
