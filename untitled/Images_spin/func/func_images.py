# -*- coding:utf-8 -*-
# 作者:周鹏
import cv2
import numpy as np
import os
from Images_spin.setting import config


class ImgSpin(object):
    scale = config.Date["scale"]

    def __init__(self, img_path, angle_list, img_save_path):
        self.img_save_path = img_save_path
        self.angle_list = angle_list
        self.img_path = img_path

    def rotate_image(self, src, angle):
        w, h = src.shape[1], src.shape[0]
        rang_r = np.deg2rad(angle)  # 弧度
        # calculate new image width and height 旋转后外接框w,h，完全包含原始图片
        nw = (abs(np.sin(rang_r) * h) + abs(np.cos(rang_r) * w)) * self.scale
        nh = (abs(np.cos(rang_r) * h) + abs(np.sin(rang_r) * w)) * self.scale
        # 旋转中心，旋转角度，缩放比例=获得仿射变化矩阵
        rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, self.scale)
        '''
        rot_mat = [[ 5.00000000e-01  8.66025404e-01 -2.07000026e+02]
                   [-8.66025404e-01  5.00000000e-01  9.10534529e+02]]
        '''
        # 外接框相对原图w，h大了多少
        het = np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0])
        # het = [      x             y            d    ]
        # het = [271.04602289  82.53451717   0.        ]
        # 如果是图片上的一个点，那么经过变化以后的坐标值为
        # (rot_mat[0][0] * x + rot_mat[0][1] * y + rot_mat[0][2], rot_mat[1][0] * x + rot_mat[1][1] * y + rot_mat[1][2])
        # 原图上面的差值根据<放射变化矩阵>算出映射后的差值
        rot_move = np.dot(rot_mat, het)
        # <放射变化矩阵>根据映射后的差值做出相应的移动
        # rot_mat[0, 2], rot_mat[1, 2]表示在x轴和y轴平移量
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # 旋转图像函数
        image = cv2.warpAffine(src, rot_mat, (int(nw), int(nh)), flags=cv2.INTER_LANCZOS4)
        return image, rot_mat, nw, nh

    def process_img(self):
        os.makedirs(self.img_save_path)
        for angle in self.angle_list:
            for img_name in os.listdir(self.img_path):
                # split filename and suffix
                n, s = os.path.splitext(img_name)
                if s == ".jpg":
                    img_path = os.path.join(self.img_path, img_name)
                    img = cv2.imread(img_path)
                    rotated_img, _, nw, nh = self.rotate_image(img, angle)
                    save_name = n + '_' + str(angle) + ".jpg"
                    # 写入图像
                    cv2.imwrite(self.img_save_path + save_name, rotated_img)
                    print("[%s] %s is processed." % (angle, img_name))


img_aug = ImgSpin(config.Date["img_path"], config.Date["spin_degree"], config.Date["crate_i"])
