# -*- coding:utf-8 -*-
# 作者:周鹏
from Images_labels_tools.config import setting
import os
import time
import cv2


def run_func_time(func):
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print()
        print('the function run {:.3f}s'.format(end - start))

    return inner


class Public(object):
    def __init__(self):
        self.img_path = setting.dict_data['images_path']
        self.lab_path = setting.dict_data['labels_path']

    def picture_operate(self):
        img_abs_path_list = []
        listdir_img = os.listdir(self.img_path)
        listdir_img.sort()
        for index in listdir_img:
            abs_path_img = os.path.join(self.img_path, index)
            img_abs_path_list.append(abs_path_img)
        return img_abs_path_list

    def file_operate(self):
        txt_abs_path_list = []
        listdir_lab = os.listdir(self.lab_path)
        listdir_lab.sort()
        for index in listdir_lab:
            abs_path_lab = os.path.join(self.lab_path, index)
            txt_abs_path_list.append(abs_path_lab)
        return txt_abs_path_list


def read_txt(r_txt_path):
    with open(r_txt_path, 'r', encoding='utf-8') as txt_file:
        coord = txt_file.readlines()
    return coord


def write_txt(w_txt_path, w_list):
    with open(w_txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.writelines(w_list)


def read_img(r_img_path):
    reads = cv2.imread(r_img_path)
    height, width, channel = reads.shape
    return height, width, channel, reads


def coordinate(c_coord_list, c_height, c_width):
    classes = c_coord_list[0]
    x_min = int((float(c_coord_list[1]) - float(c_coord_list[3]) / 2) * c_width)
    x_max = int((float(c_coord_list[1]) + float(c_coord_list[3]) / 2) * c_width)
    y_min = int((float(c_coord_list[2]) - float(c_coord_list[4]) / 2) * c_height)
    y_max = int((float(c_coord_list[2]) + float(c_coord_list[4]) / 2) * c_height)
    return classes, x_min, y_min, x_max, y_max


def str_coord(w_cls, w_x_min, w_y_min, w_x_max, w_y_max, w_height, w_width):
    x_center = round((w_x_min + (w_x_max - w_x_min) / 2) / w_width, 6)
    y_center = round((w_y_min + (w_y_max - w_y_min) / 2) / w_height, 6)
    width = round((w_x_max - w_x_min) / w_width, 6)
    height = round((w_y_max - w_y_min) / w_height, 6)
    coord_list = list(map(str, [w_cls, x_center, y_center, width, height]))
    coord_last = ' '.join(coord_list) + '\n'
    return coord_last


def read_video(r_video_path):
    images_list = []
    cap = cv2.VideoCapture(r_video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        else:
            images_list.append(frame)
    cap.release()
    return images_list


def set_saved_video(input_path, output_video, size):
    fps = 0
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    if setting.args.demo == 'video':
        input_video = cv2.VideoCapture(input_path)
        fps = int(input_video.get(cv2.CAP_PROP_FPS))
    # 图片保存为视频的FPS可以修改
    elif setting.args.demo == 'images':
        fps = 30
    video = cv2.VideoWriter(output_video, fourcc, fps, size)
    return video


def mkdir(m_path, m_new_f_name):
    path = os.path.join(os.path.dirname(m_path), m_new_f_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path
