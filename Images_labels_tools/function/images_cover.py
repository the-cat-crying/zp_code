import os
import cv2 as cv
import random
from Images_labels_tools.function import public_function
from Images_labels_tools.config import setting


# 遮盖工具
def rectangle(value_txt, argv_o, argv_t, argv_n):
    math = 1
    for x_txt in value_txt:
        path_txt = os.path.join(argv_t, x_txt)
        path_i = os.path.join(argv_o, x_txt.split('.')[0] + '.jpg')
        d_img = cv.imread(path_i)
        height, width = d_img.shape[0], d_img.shape[1]
        cover_dict, other_dict = {}, {}
        with open(path_txt, 'r', encoding='utf-8', errors='ignore') as files:
            while True:
                fs = files.readline()
                if not fs:
                    break
                else:
                    # 将遮盖部分和类别分开
                    if int(argv_n) == int(fs.split(' ')[0]):
                        cover_dict[fs] = 'labels'
                    else:
                        other_dict[fs] = 'labels'
            if len(cover_dict) < 1:  # 该图片内没有遮盖部分
                print("\r遮盖进度:{:.2%}".format(math / len(value_txt)), end='')
                math += 1
                continue
            else:
                if len(other_dict) < 1:  # 该图片内全部为遮盖部分
                    for k in cover_dict.keys():
                        x_min, y_min, x_max, y_max = coordinate(k, height, width)
                        for u in range(0, 3):
                            d_img[y_min:y_max, x_min:x_max, u] = random.randint(0, 255)
                        cv.imwrite(path_i, d_img)
                else:
                    for cy in cover_dict.keys():
                        # 矩形A左上和右下坐标
                        ax_min, ay_min, ax_max, ay_max = coordinate(cy, height, width)
                        for cy_2 in other_dict.keys():
                            # 矩形B左上和右下坐标
                            bx_min, by_min, bx_max, by_max = coordinate(cy_2, height, width)
                            # 判断遮盖和类别两个框是否为包含关系，是就进行遮盖
                            if ax_min >= bx_min and ay_min >= by_min and ax_max <= bx_max and ay_max <= by_max:
                                for h in range(0, 3):
                                    d_img[ay_min:ay_max, ax_min:ax_max, h] = random.randint(0, 255)
                                cv.imwrite(path_i, d_img)
                            else:
                                pass
                    dict_cover(cover_dict, other_dict, path_i, height=height, width=width)
                delete(path_txt, other_dict)
        print("\r开始遮盖:{:.2%}".format(math / len(value_txt)), end='')
        math += 1
    print()


# 计算X，Y坐标的最小值和最大值
def coordinate(l_str, height, width):
    x_min = round(float(l_str.split(' ')[1]) * width - float(l_str.split(' ')[3]) * width / 2)
    x_max = round(float(l_str.split(' ')[1]) * width + float(l_str.split(' ')[3]) * width / 2)
    y_min = round(float(l_str.split(' ')[2]) * height - float(l_str.strip('\n').split(' ')[4]) * height / 2)
    y_max = round(float(l_str.split(' ')[2]) * height + float(l_str.strip('\n').split(' ')[4]) * height / 2)
    return x_min, y_min, x_max, y_max


def dict_cover(cover_dict, other_dict, path_i, height, width):
    key_list, coo_ll = [], []
    img = cv.imread(path_i)
    for key in other_dict.keys():
        x_min, y_min, x_max, y_max = coordinate(key, height, width)
        coo_ll.append([y_min, y_max, x_min, x_max])
        cutout = img[y_min:y_max, x_min:x_max]
        b, g, r = cv.split(cutout)
        key_list.append([b, g, r])

    for key_c in cover_dict.keys():  # 遮盖相交部分和远离部分,以及'类别'包含在'遮盖'内的
        x_mi, y_mi, x_ma, y_ma = coordinate(key_c, height, width)
        for i in range(0, 3):
            img[y_mi:y_ma, x_mi:x_ma, i] = random.randint(0, 255)
        cv.imwrite(path_i, img)

    images_reads_s = cv.imread(path_i)
    for i_t in range(0, len(coo_ll)):  # 将之前截取的部分还原
        images_reads_s[coo_ll[i_t][0]:coo_ll[i_t][1], coo_ll[i_t][2]:coo_ll[i_t][3]] = cv.merge(key_list[i_t])
        cv.imwrite(path_i, images_reads_s)


def delete(path_txt, other_dict):  # 将遮盖部分的文本内容删掉
    list_test = [p for p in other_dict.keys()]
    with open(path_txt, 'w', encoding='utf-8', errors='ignore') as new_file:
        # writelines()既可以传入字符串又可以传入一个字符序列,并将该字符序列写入文件,必须传入的是字符序列,不能是数字序列
        new_file.writelines(list_test)


def main():
    argv_1 = public_function.Public().img_path  # images路径
    argv_2 = public_function.Public().lab_path  # labels路径
    argv_3 = setting.dict_cover['category']  # 需要遮盖的类别(数字)
    list_txt = os.listdir(argv_2)
    list_txt.sort()
    return argv_1, argv_2, argv_3, list_txt


def start_main():
    argv_one, argv_two, argv_three, list_txt = main()
    rectangle(value_txt=list_txt, argv_o=argv_one, argv_t=argv_two, argv_n=argv_three)
    print('\n')
    print('images保存在: {0}'.format(argv_one))
    print('labels保存在: {0}'.format(argv_two))
