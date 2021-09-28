import random
import numpy
import tqdm
import time
import os
import cv2
from Images_labels_tools.function import public_function


def rand(r_x_min, r_y_min, r_x_max, r_y_max):
    x_min = random.randint(r_x_min, r_x_max)
    y_min = random.randint(r_y_min, r_y_max)
    index1 = r_x_max - (r_x_max - r_x_min) // 2
    x_1 = random.randint(r_x_min, index1)
    index2 = r_y_max - (r_y_max - r_y_min) // 2
    y_1 = random.randint(r_y_min, index2)
    x_max = numpy.clip(x_min + x_1, r_x_min, r_x_max)
    y_max = numpy.clip(y_min + y_1, r_y_min, r_y_max)
    return x_min, y_min, x_max, y_max


def cutout(c_argv_1, c_argv_2, c_time_str):
    for i in tqdm.tqdm(c_argv_1):
        height, width, channel, img = public_function.read_img(i)
        lab = i.replace('images', 'labels', 1)
        lab = lab.replace('.jpg', '.txt', 1)
        txt_list = public_function.read_txt(lab)
        file_path, name = os.path.split(i)
        abs_img_path = save_path(c_argv_2, name, c_time_str)
        for j in txt_list:
            j_split = j.strip('\n').split(' ')
            classes, x_min, y_min, x_max, y_max = public_function.coordinate(j_split, height, width)
            if random.sample([0, 1], 1):
                m_x_min, m_y_min, m_x_max, m_y_max = rand(x_min, y_min, x_max, y_max)
                area = (y_max - y_min) * (x_max - x_min)
                mask_area = (m_x_max - m_x_min) * (m_y_max - m_y_min)
                if area / 8 <= mask_area <= area / 2:
                    img[m_y_min:m_y_max, m_x_min:m_x_max, :] = 0
        cv2.imwrite(abs_img_path, img)


def save_path(s_argv, s_name, s_time_str):
    img_path = public_function.mkdir(s_argv, s_time_str + '_cutout_images')
    abs_img_path = os.path.join(img_path, s_name)
    return abs_img_path


def start():
    argv_1 = public_function.Public().picture_operate()
    argv_2 = public_function.Public().img_path
    time_s = time.localtime()
    time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time_s)
    cutout(argv_1, argv_2, time_str)
