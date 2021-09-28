import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


e = cv.imread('/home/zhoup/work/yolomark/img/20200506_work/images/000001.jpg')
img = cv.resize(e, (0, 0), fx=0.4, fy=0.4)
data = img.reshape((-1, 3))
data = np.float32(data)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
k = 5
ret, label, center = cv.kmeans(data, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
print(center)
print(label)
print(label.flatten())
res1 = center[label.flatten()]
print(res1)
res2 = res1.reshape(img.shape)

plt.subplot(121)
plt.imshow(img, cmap='gray')
plt.title('gg')
plt.axis('off')

plt.subplot(122)
plt.imshow(res2, cmap='gray')
plt.title('jj')
plt.axis('off')

plt.show()
