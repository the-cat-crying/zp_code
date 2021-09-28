#!/usr/bin/env python
import cv2
import numpy as np
import os
from Images_spin.setting import config


class Compute(object):
    scale = config.Date["scale"]

    def __init__(self, src, angle):
        self.src = src
        self.angle = angle

    def rotate_image(self):
        w = self.src.shape[1]
        h = self.src.shape[0]
        rang_r = np.deg2rad(self.angle)
        nw = (abs(np.sin(rang_r) * h) + abs(np.cos(rang_r) * w)) * self.scale
        nh = (abs(np.cos(rang_r) * h) + abs(np.sin(rang_r) * w)) * self.scale
        rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), self.angle, self.scale)
        het = np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0])
        rot_move = np.dot(rot_mat, het)
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        image = cv2.warpAffine(self.src, rot_mat, (int(nw), int(nh)), flags=cv2.INTER_LANCZOS4)
        return image, rot_mat, nw, nh

    def rotate_xml(self, x_min, y_min, x_max, y_max):
        _, rot_mat, _, _ = self.rotate_image()
        point1 = np.dot(rot_mat, np.array([(x_min + x_max) / 2, y_min, 1]))
        point2 = np.dot(rot_mat, np.array([x_max, (y_min + y_max) / 2, 1]))
        point3 = np.dot(rot_mat, np.array([(x_min + x_max) / 2, y_max, 1]))
        point4 = np.dot(rot_mat, np.array([x_min, (y_min + y_max) / 2, 1]))
        concat = np.vstack((point1, point2, point3, point4))
        concat = concat.astype(np.int32)
        rx, ry, rw, rh = cv2.boundingRect(concat)
        return rx, ry, rw, rh


class ImgSpin(Compute):
    def __init__(self, img_path, tables_path, angle_list, img_save_path, tables_save_path, src, angle):
        super().__init__(src, angle)
        self.tables_save_path = tables_save_path
        self.img_save_path = img_save_path
        self.angle_list = angle_list
        self.tables_path = tables_path
        self.img_path = img_path

    def process_img(self):
        os.makedirs(self.img_save_path)
        os.makedirs(self.tables_save_path)
        for angle in self.angle_list:
            for img_name in os.listdir(self.img_path):
                n, s = os.path.splitext(img_name)
                if s == ".jpg":
                    img_path = os.path.join(self.img_path, img_name)
                    img = cv2.imread(img_path)
                    super(ImgSpin, self).__init__(src=img, angle=angle)
                    rotated_img, _, nw, nh = super(ImgSpin, self).rotate_image()
                    save_name = n + '_' + str(angle) + ".jpg"
                    cv2.imwrite(self.img_save_path + save_name, rotated_img)
                    new_tables = self.process_tables(n, img, nw, nh)
                    save_path = os.path.join(self.tables_save_path + n + '_' + str(angle) + ".txt")
                    with open(save_path, 'w', encoding='utf-8') as g:
                        g.writelines(new_tables)
                    print("[%s] %s is processed." % (angle, img_name))

    def process_tables(self, n, img, nw, nh):
        new_tables = []
        tree = os.path.join(self.tables_path, n + '.txt')
        with open(tree, 'r', encoding='utf-8') as f:
            for i in f:
                category, x_c, y_c, w_c, h_c = i.split(' ')[0], float(i.split(' ')[1]), float(i.split(' ')[2]),\
                                               float(i.split(' ')[3]), float(i.strip('\n').split(' ')[4])
                width, height = float(img.shape[1]), float(img.shape[0])
                x_min = int((x_c - w_c / 2) * width)
                x_max = int((x_c + w_c / 2) * width)
                y_min = int((y_c - h_c / 2) * height)
                y_max = int((h_c + h_c / 2) * height)
                x, y, w, h = super(ImgSpin, self).rotate_xml(x_min, y_min, x_max, y_max)
                x_cen, y_cen = round((x + w / 2) / nw, 6), round((y + h / 2) / nh, 6)
                w_cen, h_cen = round(w / nw, 6), round(h / nh, 6)
                new_tables.append(' '.join([category, str(x_cen), str(y_cen), str(w_cen), str(h_cen) + '\n']))
        return new_tables


img_aug = ImgSpin(config.Date["img_path"], config.Date["tables_path"], config.Date["spin_degree"],
                  config.Date["crate_i"], config.Date["crate_t"], 0, 0)
