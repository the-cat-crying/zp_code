import cv2
import os

a = '/home/gy/mount_sdc/from_testing_division/20210907_from_xwy_Y33_test_set/Y33_模拟识别/Y33_直升机_small'
c = os.listdir(a)
c.sort()
for i in c:
    p = os.path.join(a, i)
    img = cv2.imread(p)
    # (3, 3)表示高斯滤波器的长和宽都为3，1.5表示滤波器的标准差
    out = cv2.GaussianBlur(img, (5, 3), 0)
    cv2.imwrite(os.path.join('/home/gy/mount_sdc/from_testing_division/20210907_from_xwy_Y33_test_set/Y33_模拟识别/Y33_直升机_small_gauss/' + i), out)
    cv2.imshow('result', out)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
