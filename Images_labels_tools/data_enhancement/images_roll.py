import os
import sys
import cv2 as cv
import numpy as np
import datetime
from Images_labels_tools.function.public_function import run_func_time


# 所有图片的高和宽
def read_img(img, argv_1_g):
    images = []
    for h_s in img:
        image = cv.imread(os.path.join(argv_1_g, h_s))
        h, w = image.shape[0], image.shape[1]
        images.append([h, w])
    return images


# 所有图片和边界框分别写如一个列表
def read_txt(path_txt, argv_1_t, argv_1_i):
    box_all_list, image_all_list = [], []
    for i_txt in path_txt:
        img_path = os.path.join(argv_1_t, i_txt.split('.')[0] + '.jpg')
        path = os.path.join(argv_1_i, i_txt)
        box_1, image_1 = [], []
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for read_line in f:
                box_1.extend([read_line.split(' ')[0], read_line.split(' ')[1], read_line.split(' ')[2],
                              read_line.split(' ')[3], read_line.strip('\n').split(' ')[4]])
            image_1.append(cv.imread(img_path))
        image_all_list.append(image_1)
        box_all_list.append(box_1)
    return box_all_list, image_all_list


# 所有图片和边界框的移动操作
@run_func_time
def move_img(img_path, txt_path, number, argv, argv_s):
    g = int(input('请输入数字需要的方向,1 横向，2 纵向 : '))
    image_all = read_img(img_path, argv)
    box_s, image_s = read_txt(txt_path, argv, argv_s)
    # 时间字符串格式化
    time_clock = datetime.datetime.now().strftime('%Y.%m.%d_%H:%M:%S')
    # dirname获取images上一层目录路径
    abs_path = os.path.dirname(argv)
    # 创建文件夹
    os.makedirs(os.path.join(abs_path, 'images_' + time_clock))
    os.makedirs(os.path.join(abs_path, 'labels_' + time_clock))
    if g == 1:
        index_x = [1, 3]
        move(number, box_s, image_all, abs_path, time_clock, txt_path, image_s, g, index_x)
    else:
        index_y = [2, 4]
        move(number, box_s, image_all, abs_path, time_clock, txt_path, image_s, g, index_y)
    print('\n')
    print('images保存在{0}'.format(os.path.join(abs_path, 'images_' + time_clock)))
    print('labels保存在{0}'.format(os.path.join(abs_path, 'labels_' + time_clock)))


def move(number_g, box_g, image_ag, abs_g, time_g, txt_g, image_sg, g_g, index_g):
    num = 1
    while num <= number_g:
        for i in range(0, len(box_g)):
            h_s, w_s = int(image_ag[i][0]), int(image_ag[i][1])
            if g_g == 1:
                length = w_s
            else:
                length = h_s
            # 把图片分成移动次数加一块
            removing = round(length / (number_g + 1))
            moving_line = length - removing * num
            bounding_box = []
            for b in range(0, int(len(box_g[i]) / 5)):
                cor_min = round(float(box_g[i][index_g[0] + b * 5]) * length - float(box_g[i][index_g[1] + b * 5]) *
                                length / 2)
                cor_max = round(float(box_g[i][index_g[0] + b * 5]) * length + float(box_g[i][index_g[1] + b * 5]) *
                                length / 2)
                # 比较移动边界线和边界框的位置
                if cor_min < moving_line < cor_max:
                    new_coordinate_1(box_g, length, removing, bounding_box, num, cor_min, i, b, g_g)
                elif moving_line >= cor_max:
                    new_coordinate_2(box_g, length, removing, bounding_box, num, i, b, g_g)
                elif moving_line <= cor_min:
                    new_coordinate_3(box_g, length, moving_line, bounding_box, i, b, g_g)
                else:
                    pass
            # 将更改后的坐标值从新写入新的文档
            with open(os.path.join(abs_g, 'labels_' + time_g, '0' + str(num) + '_' + txt_g[i]), 'w') as f_w:
                f_w.writelines(bounding_box)
            cover_img = cv.merge(image_sg[i])
            if g_g == 1:
                # 将图片水平合并
                img3 = np.hstack([cover_img[:, moving_line:length], cover_img[:, 0:moving_line]])
                cv.imwrite(os.path.join(abs_g, 'images_' + time_g, '0' + str(num) + '_' + txt_g[i].split('.')[0]
                                        + '.jpg'), img3)
            else:
                # 将图片纵向合并
                img3 = np.vstack([cover_img[moving_line:length, :], cover_img[0:moving_line, :]])
                cv.imwrite(os.path.join(abs_g, 'images_' + time_g, '0' + str(num) + '_' + txt_g[i].split('.')[0]
                                        + '.jpg'), img3)
            print('\r{:.2%}'.format(num / number_g), end='')
        num += 1


# 新坐标
def new_coordinate_1(box_x, hw_x, remove_x, box_copy_x, num_x, x_min_x, i_x, b_x, g_x):
    if g_x == 1:
        w_h = float(box_x[i_x][3 + b_x * 5])
    else:
        w_h = float(box_x[i_x][4 + b_x * 5])
    w_h_length = round(w_h * hw_x)
    new_w_left = round((hw_x - remove_x * num_x - x_min_x) / hw_x, 6)
    new_x_left_c = round((x_min_x + (hw_x - remove_x * num_x - x_min_x) / 2 + remove_x * num_x) / hw_x, 6)

    new_w_right = round((w_h_length - (hw_x - remove_x * num_x - x_min_x)) / hw_x, 6)
    new_x_right_c = round(((w_h_length - (hw_x - remove_x * num_x - x_min_x)) / 2) / hw_x, 6)
    # 新的两个框坐标值
    if g_x == 1:
        box_copy_x.append(' '.join([box_x[i_x][0 + b_x * 5], str(new_x_left_c), box_x[i_x][2 + b_x * 5],
                                    str(new_w_left), box_x[i_x][4 + b_x * 5]]) + '\n')  # join以什么形式拼接成字符串
        box_copy_x.append(box_x[i_x][0 + b_x * 5] + ' ' + str(new_x_right_c) + ' ' + box_x[i_x][2 + b_x * 5] + ' ' +
                          str(new_w_right) + ' ' + box_x[i_x][4 + b_x * 5] + '\n')
    else:
        new_normalized_1 = box_x[i_x][0 + b_x * 5] + ' ' + box_x[i_x][1 + b_x * 5] + ' ' + str(new_x_left_c) + ' ' + \
            box_x[i_x][3 + b_x * 5] + ' ' + str(new_w_left) + '\n'
        new_normalized_2 = ' '.join([box_x[i_x][0 + b_x * 5], box_x[i_x][1 + b_x * 5], str(new_x_right_c),
                                     box_x[i_x][3 + b_x * 5], str(new_w_right)]) + '\n'
        box_copy_x.append(new_normalized_1)
        box_copy_x.append(new_normalized_2)


def new_coordinate_2(box_g, hw_g, remove_g, box_copy_g, num_g, i_g, b_g, g_g):
    if g_g == 1:
        old = float(box_g[i_g][1 + b_g * 5])
    else:
        old = float(box_g[i_g][2 + b_g * 5])
    new_x = round((round(old * hw_g) + remove_g * num_g) / hw_g, 6)
    if g_g == 1:
        box_copy_g.append(' '.join([box_g[i_g][0 + b_g * 5], str(new_x), box_g[i_g][2 + b_g * 5],
                                    box_g[i_g][3 + b_g * 5], box_g[i_g][4 + b_g * 5]]) + '\n')
    else:
        box_copy_g.append(box_g[i_g][0 + b_g * 5] + ' ' + box_g[i_g][1 + b_g * 5] + ' ' + str(new_x) + ' ' +
                          box_g[i_g][3 + b_g * 5] + ' ' + box_g[i_g][4 + b_g * 5] + '\n')


def new_coordinate_3(box_f, hw_f, moving_f, box_copy_f, i_f, b_f, g_f):
    if g_f == 1:
        old_f = float(box_f[i_f][1 + b_f * 5])
    else:
        old_f = float(box_f[i_f][2 + b_f * 5])
    moving_x = round(old_f * hw_f) - moving_f
    new_f = round(moving_x / hw_f, 6)
    if g_f == 1:
        box_copy_f.append(box_f[i_f][0 + b_f * 5] + ' ' + str(new_f) + ' ' + box_f[i_f][2 + b_f * 5] + ' ' +
                          box_f[i_f][3 + b_f * 5] + ' ' + box_f[i_f][4 + b_f * 5] + '\n')
    else:
        box_copy_f.append(' '.join([box_f[i_f][0 + b_f * 5], box_f[i_f][1 + b_f * 5], str(new_f),
                                    box_f[i_f][3 + b_f * 5], box_f[i_f][4 + b_f * 5]]) + '\n')


def main_n():
    if len(sys.argv) != 4:
        print('请依次输入<images,labels路径>和<移动次数>')
        sys.exit(0)
    else:
        argv_1 = sys.argv[1]  # images
        argv_2 = sys.argv[2]  # labels
        argv_3 = int(sys.argv[3])  # 切割次数n，0<n<image.width
        image_list = os.listdir(argv_1)
        image_list.sort()
        txt_list = os.listdir(argv_2)
        txt_list.sort()
    return argv_1, argv_2, argv_3, image_list, txt_list


def main():
    argv_1, argv_2, argv_3, image_list, txt_list = main_n()
    move_img(image_list, txt_list, argv_3, argv_1, argv_2)


if __name__ == '__main__':
    # 图像卷积移动
    main()
