# -*- coding:utf-8 -*-

import cv2 as cv
import os
import sys
import time
import datetime


def run_time(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print('operation hours {0:.3f}'.format(end_time - start_time))
    return inner


def img_list(images):
    # 所有图片中的所有框到各边的距离总集合
    x_left_list, x_right_list, y_up_list, y_down_list = [], [], [], []
    for a in images:
        path_images = os.path.join(argv_1, a)
        read_images = cv.imread(path_images)
        height, width = read_images.shape[0], read_images.shape[1]
        path_labels = os.path.join(argv_2, a.split('.')[0] + '.txt')   # labels绝对路径获取
        # 传入要读的文件路径
        with open(path_labels, "r", encoding="utf-8", errors="ignore") as file:
            # 每个框各边到图像各边的距离
            left, right, up, down = [], [], [], []
            while True:
                # 表示一次读取一行
                my_str = file.readline()
                # 读到数据my_str为空的时候，结束循环。数据的最后也就是读不到数据了.
                if not my_str:
                    break
                else:
                    # x,y中心坐标值,w,h为高和宽
                    x_center = float(my_str.split(' ')[1]) * width
                    y_center = float(my_str.split(' ')[2]) * height
                    w_length = float(my_str.split(' ')[3]) * width
                    # strip用来去除头尾字符、空白符(包括\n、\r、\t、' '，即：换行、回车、制表符、空格)
                    h_length = float(my_str.strip('\n').split(' ')[4]) * height

                    x_min = x_center - w_length / 2
                    left.append(x_min)  # append在元素在末尾增加元素
                    right.append(width - w_length - x_min)
                    y_min = y_center - h_length / 2
                    up.append(y_min)
                    down.append(height - h_length - y_min)
            # 写入一个列表表示一个张图
            x_left_list.append(left)
            x_right_list.append(right)
            y_up_list.append(up)
            y_down_list.append(down)
    # 返回标签到图像四边的距离
    return x_left_list, x_right_list, y_up_list, y_down_list


def coordinates(path, denominator, molecular_x, molecular_y):
    # 新坐标生成写入
    with open(path, 'r', encoding='utf-8', errors='ignore') as files_1:
        # readlines()读取全部行，为一个列表
        last = files_1.readlines()
        for line in last:
            split_0 = line.split(' ')[0]
            split_1 = line.split(' ')[1]
            split_2 = line.split(' ')[2]
            split_3 = line.split(' ')[3]
            split_4 = line.strip('\n').split(' ')[4]
            new_x_center = round((round(float(split_1)) - molecular_x) / denominator, 6)
            new_y_center = round((round(float(split_2)) - molecular_y) / denominator, 6)
            new_width = round(round(float(split_3)) / denominator, 6)
            new_height = round(round(float(split_4)) / denominator, 6)
            last_str = split_0 + ' ' + str(new_x_center) + ' ' + str(new_y_center) + ' ' + str(new_width) + ' ' \
                + str(new_height) + '\n'
            with open(path, 'r', encoding='utf-8', errors='ignore') as files_last:
                # 文本内容完全读取并替换其中需求项
                k = files_last.read().replace(line, last_str, 1)
            with open(path, 'w', encoding='utf-8', errors='ignore') as files_last_s:
                # 新数据先清空在写入全部数据
                files_last_s.write(k)


@run_time
def screenshots(head, demo):
    x_left, x_right, y_up, y_down = head
    # 每张图片内所有框到对应边最小值集合
    min_left_all, min_right_all, min_up_all, min_down_all = [], [], [], []
    for i_left in x_left:
        left_distance = min(i_left)
        min_left_all.append(left_distance)
    for i_right in x_right:
        right_distance = min(i_right)
        min_right_all.append(right_distance)
    for i_up in y_up:
        up_distance = min(i_up)
        min_up_all.append(up_distance)
    for i_down in y_down:
        down_distance = min(i_down)
        min_down_all.append(down_distance)
    # 时间字符串格式化
    time_clock = datetime.datetime.now().strftime('%Y.%m.%d_%H:%M:%S')
    # dirname获取images上一层目录路径
    abs_path = os.path.dirname(argv_1)
    os.makedirs(os.path.join(abs_path, 'images_' + time_clock))

    num = 0
    for h in demo:
        save_path = os.path.join(abs_path, 'images_' + time_clock, h.split('.')[0] + '.jpg')
        file_path = os.path.join(argv_2, h.split('.')[0] + '.txt')
        path_h = os.path.join(argv_1, h)

        images = cv.imread(path_h)
        height_1, width_1 = images.shape[0], images.shape[1]
        # round函数保留整数部分,小数部分四舍五入
        x_min_line = round(min_left_all[num])
        x_max_line = round(width_1 - min_right_all[num])
        y_min_column = round(min_up_all[num])
        y_max_column = round(height_1 - min_down_all[num])
        # 预剪切出原图片包含所有框大小
        x_poor = x_max_line - x_min_line
        y_poor = y_max_column - y_min_column
        # 坐标还原
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as files:
            file_read = files.readlines()
            for j in file_read:
                y_centers = float(j.split(' ')[2]) * height_1
                x_centers = float(j.split(' ')[1]) * width_1
                w_real = float(j.split(' ')[3]) * width_1
                h_real = float(j.strip('\n').split(' ')[4]) * height_1
                new_str = j.split(' ')[0] + ' ' + str(x_centers) + ' ' + str(y_centers) + ' ' + str(w_real) + ' ' + \
                    str(h_real) + '\n'
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as files_s:
                    x = files_s.read()
                    re_value = x.replace(j, new_str, 1)
                with open(file_path, 'w', encoding='utf-8', errors='ignore') as files_ss:
                    files_ss.write(re_value)
        # 通过比较剪切出的h和w真实大小长度,结果都调整为正方形
        if y_poor < x_poor:
            # 剪切图片w和原图片的h比较
            if x_poor <= height_1:
                # 剪切图片的w和剪切的y的最大值比较
                if x_poor <= y_max_column:
                    y_min_column_new = y_max_column - x_poor
                    new_image_1 = images[y_min_column_new:y_max_column, x_min_line:x_max_line]
                    # 图像存储
                    cv.imwrite(save_path, new_image_1)
                    coordinates(path=file_path, denominator=x_poor, molecular_x=x_min_line,
                                molecular_y=y_min_column_new)
                else:
                    new_image_2 = images[0:x_poor, x_min_line:x_max_line]
                    cv.imwrite(save_path, new_image_2)
                    coordinates(path=file_path, denominator=x_poor, molecular_x=x_min_line, molecular_y=0)
            else:
                new_image_3 = images[0:height_1, x_min_line:x_max_line]
                fill = x_poor - height_1
                new_image_4 = cv.copyMakeBorder(new_image_3, round(fill/2), fill-round(fill/2), 0, 0,
                                                cv.BORDER_CONSTANT, value=(255, 255, 255))
                cv.imwrite(save_path, new_image_4)
                coordinates(path=file_path, denominator=x_poor, molecular_x=x_min_line, molecular_y=-round(fill/2))
        elif y_poor > x_poor:
            if y_poor <= width_1:
                if y_poor <= x_max_line:
                    x_min_line_new = x_max_line - y_poor
                    new_image_5 = images[y_min_column:y_max_column, x_min_line_new:x_max_line]
                    cv.imwrite(save_path, new_image_5)
                    coordinates(path=file_path, denominator=y_poor, molecular_x=x_min_line_new,
                                molecular_y=y_min_column)
                else:
                    new_image_6 = images[y_min_column:y_max_column, 0:y_poor]
                    cv.imwrite(save_path, new_image_6)
                    coordinates(path=file_path, denominator=y_poor, molecular_x=0, molecular_y=y_min_column)
            else:
                new_image_7 = images[y_min_column:y_max_column, 0:width_1]
                fill_1 = y_poor - width_1
                new_image_8 = cv.copyMakeBorder(new_image_7, 0, 0, round(fill_1/2), fill_1-round(fill_1/2),
                                                cv.BORDER_CONSTANT, value=(255, 255, 255))
                cv.imwrite(save_path, new_image_8)
                coordinates(path=file_path, denominator=y_poor, molecular_x=-round(fill_1/2), molecular_y=y_min_column)
        else:
            new_image_9 = images[y_min_column:y_max_column, x_min_line:x_max_line]
            cv.imwrite(save_path, new_image_9)
            coordinates(path=file_path, denominator=y_poor, molecular_x=x_min_line, molecular_y=y_min_column)
        # 转义字符\r表示在首行首列打印，end=''表示输出不换行
        print('\r{:.2%}'.format((num+1)/len(listdir_1)), end='')
        num += 1


if __name__ == '__main__':
    # 图片剪切为一个正方形
    start = time.time()
    argv_1 = sys.argv[1]  # images路径
    argv_2 = sys.argv[2]  # labels路径
    # cut start
    listdir_1 = os.listdir(argv_1)
    listdir_1.sort()
    listdir_2 = os.listdir(argv_2)
    listdir_2.sort()
    # 返回所有标签到图像四周的距离
    distance_list = img_list(images=listdir_1)
    screenshots(head=distance_list, demo=listdir_1)
