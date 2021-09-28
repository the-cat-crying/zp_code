import random
import cv2
import numpy
import os
import time
from Images_labels_tools.function import public_function


def coord(c_width, c_height):
    x_min = random.randint(0, c_width)
    y_min = random.randint(0, c_height)
    index1 = random.randint(0, c_width // 2)
    index2 = random.randint(0, c_height // 2)
    x_max = numpy.clip(x_min + index1, 0, c_width)
    y_max = numpy.clip(y_min + index2, 0, c_height)
    return x_min, y_min, x_max, y_max


def cut_mix(c_argv_1, c_argv_2, c_argv_3, c_time_str):
    zip_list = list(zip(c_argv_1, c_argv_2))
    len_ = len(os.listdir(c_argv_3))
    number = 0
    while True:
        if len(zip_list) == 0 or len(zip_list) == 1:
            break
        else:
            sam = random.sample(zip_list, 2)
            sam_1 = random.sample(sam, 1)
            height, width, channel, reads = public_function.read_img(sam_1[0][0])
            x_min, y_min, x_max, y_max = coord(width, height)
            t_list = [x_min, y_min, x_max, y_max]
            value_x = x_max - x_min
            value_y = y_max - y_min
            coord_all_list = []
            for i in sam:
                if i in sam_1:
                    continue
                else:
                    height_2, width_2, channel_2, reads_2 = public_function.read_img(i[0])
                    value_x, value_y, t_list = judge(value_x, value_y, t_list, height_2, width_2)
                    x2_min = random.randint(0, width_2 // 2)
                    y2_min = random.randint(0, height_2 // 2)
                    x2_max = x2_min + value_x
                    y2_max = y2_min + value_y

                    x2_max = numpy.clip(x2_max, 0, width_2)
                    y2_max = numpy.clip(y2_max, 0, height_2)
                    x2_min = x2_max - value_x
                    y2_min = y2_max - value_y
                    t_list2 = [x2_min, y2_min, x2_max, y2_max]
                    coord_all_list = txt_read(i[1], height_2, width_2, t_list, t_list2, coord_all_list, height, width)
                    coord_all_list = txt_read2(sam_1[0][1], height, width, t_list, coord_all_list)
                    reads[t_list[1]:t_list[3], t_list[0]:t_list[2]] = reads_2[t_list2[1]:t_list2[3], t_list2[0]:t_list2[2]]
                    abs_img_path, abs_lab_path = mkdir_path(c_argv_3, number, c_time_str)
                    cv2.imwrite(abs_img_path, reads)
                    public_function.write_txt(abs_lab_path, coord_all_list)
            zip_list.remove(sam[0])
            zip_list.remove(sam[1])
            number += 2
        print('\rcutmix进度: {0:.2%}'.format(number / len_), end='')


def judge(j_value1, j_value2, j_list1, j_h, j_w):
    j_value1 = numpy.clip(j_value1, 0, j_w)
    j_value2 = numpy.clip(j_value2, 0, j_h)
    j_list1[2] = j_list1[0] + j_value1
    j_list1[3] = j_list1[1] + j_value2
    return j_value1, j_value2, j_list1


def txt_read(t_path, t_height, t_width, t_list_1, t_list, coord_all_list, t_h, t_w):
    txt_list = public_function.read_txt(t_path)
    for i in txt_list:
        i_split = i.strip('\n').split(' ')
        classes, x_min, y_min, x_max, y_max = public_function.coordinate(i_split, t_height, t_width)
        if x_max <= t_list[0] or x_min >= t_list[2] or y_max <= t_list[1] or y_min >= t_list[3]:
            continue
        else:
            x_min = numpy.clip(x_min, t_list[0], t_list[2])
            x_max = numpy.clip(x_max, t_list[0], t_list[2])
            y_min = numpy.clip(y_min, t_list[1], t_list[3])
            y_max = numpy.clip(y_max, t_list[1], t_list[3])

            x_min = x_min - t_list[0] + t_list_1[0]
            x_max = x_max - t_list[0] + t_list_1[0]
            y_min = y_min - t_list[1] + t_list_1[1]
            y_max = y_max - t_list[1] + t_list_1[1]
        coord_last = public_function.str_coord(classes, x_min, y_min, x_max, y_max, t_h, t_w)
        coord_all_list.append(coord_last)
    return coord_all_list


def txt_read2(t_path, t_height, t_width, t_list, coord_all_list):
    txt_list2 = public_function.read_txt(t_path)
    for j in txt_list2:
        j_split = j.strip('\n').split(' ')
        classes, x_min, y_min, x_max, y_max = public_function.coordinate(j_split, t_height, t_width)
        if t_list[0] <= x_min < x_max <= t_list[2] and t_list[1] <= y_min < y_max <= t_list[3]:
            continue
        elif t_list[0] <= x_min < x_max <= t_list[2] and y_min < t_list[1] < y_max <= t_list[3]:
            y_max = t_list[0]
            coord_last = public_function.str_coord(classes, x_min, y_min, x_max, y_max, t_height, t_width)
            coord_all_list.append(coord_last)
        elif t_list[0] <= x_min < x_max <= t_list[2] and t_list[1] <= y_min < t_list[3] < y_max:
            y_min = t_list[3]
            coord_last = public_function.str_coord(classes, x_min, y_min, x_max, y_max, t_height, t_width)
            coord_all_list.append(coord_last)
        elif x_min < t_list[0] < x_max <= t_list[2] and t_list[1] <= y_min < y_max <= t_list[3]:
            x_max = t_list[0]
            coord_last = public_function.str_coord(classes, x_min, y_min, x_max, y_max, t_height, t_width)
            coord_all_list.append(coord_last)
        elif t_list[0] <= x_min < t_list[2] < x_max and t_list[1] <= y_min < y_max <= t_list[3]:
            x_min = t_list[2]
            coord_last = public_function.str_coord(classes, x_min, y_min, x_max, y_max, t_height, t_width)
            coord_all_list.append(coord_last)
        else:
            coord_all_list.append(j)
    return coord_all_list


def mkdir_path(m_path, m_number, m_c_time_str):
    img_path = public_function.mkdir(m_path, m_c_time_str + '_cutmix_images')
    lab_path = public_function.mkdir(m_path, m_c_time_str + '_cutmix_labels')
    abs_img_path = os.path.join(img_path, str(m_number) + '.jpg')
    abs_lab_path = os.path.join(lab_path, str(m_number) + '.txt')
    return abs_img_path, abs_lab_path


def start():
    argv_1 = public_function.Public().picture_operate()
    argv_2 = public_function.Public().file_operate()
    argv_3 = public_function.Public().img_path
    time_s = time.localtime()
    time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time_s)
    cut_mix(argv_1, argv_2, argv_3, time_str)
