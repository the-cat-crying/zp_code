import os
import sys
import time
import cv2 as cv
import random


# 时间运行函数-装饰器
def print_run_time(func):
    def wrapper(*args, **kwargs):
        local_time = time.time()
        func(*args, **kwargs)
        print('\n')
        print('--current function [%s] run time is %.3fs\n' % (func.__name__, time.time() - local_time))
    return wrapper


# 对于较小目标进行操作
@print_run_time
def run(number, p_txt_dir, amount):
    go = 1
    for i in p_txt_dir:
        list_cover = []
        list_not_cover = []
        path_txt = os.path.join(sys.argv[2], i)
        path_img = os.path.join(sys.argv[1], i.split('.')[0] + '.jpg')
        image_read = cv.imread(path_img)
        height, width = image_read.shape[0], image_read.shape[1]
        with open(path_txt, 'r', encoding='utf-8', errors='ignore') as f:
            while True:
                f_l = f.readline()
                if not f_l:
                    break
                else:
                    cate, x_cen, y_cen, width_s, height_s = f_l.split(' ')[0], f_l.split(' ')[1], f_l.split(' ')[2],\
                                                            f_l.split(' ')[3], f_l.strip('\n').split(' ')[4]
                    # 面积比
                    percentage = round(float(width_s) * float(height_s), 5)
                    # 占比千分之几比较
                    if percentage * 1000 <= int(number):
                        list_cover.append([cate, x_cen, y_cen, width_s, height_s])
                    else:
                        list_not_cover.append([cate, x_cen, y_cen, width_s, height_s])
            if len(list_cover) == 0:
                continue
            else:
                if len(list_not_cover) == 0:
                    for p in range(0, len(list_cover)):
                        x_min_p, x_max_p, y_min_p, y_max_p = size(height, width, list_cover, p)
                        image_read[y_min_p:y_max_p, x_min_p:x_max_p, 0] = random.randint(1, 254)
                        image_read[y_min_p:y_max_p, x_min_p:x_max_p, 1] = random.randint(0, 255)
                        image_read[y_min_p:y_max_p, x_min_p:x_max_p, 2] = random.randint(0, 255)
                        cv.imwrite(path_img, image_read)
                        doc(path_txt, list_cover, p)
                else:
                    if 1 == amount:
                        for j in range(0, len(list_cover)):
                            x_min_c, x_max_c, y_min_c, y_max_c = size(height, width, list_cover, j)
                            for k in range(0, len(list_not_cover)):
                                x_min_n, x_max_n, y_min_n, y_max_n = size(height, width, list_not_cover, k)
                                if x_min_c >= x_min_n and x_max_c >= x_max_n and y_min_c <= y_min_n \
                                        and y_max_c <= y_max_n:
                                    image_read[y_min_c:y_max_c, x_min_c:x_max_c, 0] = random.randint(2, 255)
                                    image_read[y_min_c:y_max_c, x_min_c:x_max_c, 1] = random.randint(0, 255)
                                    image_read[y_min_c:y_max_c, x_min_c:x_max_c, 2] = random.randint(0, 255)
                                    cv.imwrite(path_img, image_read)
                                    doc(path_txt, list_cover, j)
                                else:
                                    pass
                        cover(height, width, list_cover, list_not_cover, path_txt, path_img, image_read)
                    else:
                        for x in range(0, len(list_cover)):
                            doc(path_txt, list_cover, x)
            print('\r{:.2%}'.format(go / len(path_txt)), end='')
            go += 1


def cover(height_c, width_c, list_c, list_nc, path_c, path_ic, img_c):
    list_h, list_num = [], []
    for h in range(0, len(list_nc)):
        x_min_h, x_max_h, y_min_h, y_max_h = size(height_c, width_c, list_nc, h)
        list_num.append([x_min_h, x_max_h, y_min_h, y_max_h])
        list_h.append(img_c[y_min_h:y_max_h, x_min_h:x_max_h])
    for t in range(0, len(list_c)):
        x_min_t, x_max_t, y_min_t, y_max_t = size(height_c, width_c, list_c, t)
        img_c[y_min_t:y_max_t, x_min_t:x_max_t, 0] = random.randint(1, 255)
        img_c[y_min_t:y_max_t, x_min_t:x_max_t, 1] = random.randint(0, 255)
        img_c[y_min_t:y_max_t, x_min_t:x_max_t, 2] = random.randint(0, 255)
        cv.imwrite(path_ic, img_c)
        doc(path_c, list_c, t)
    new_img = cv.imread(path_ic)
    for x in range(0, len(list_num)):
        new_img[list_num[x][2]:list_num[x][3], list_num[x][0]:list_num[x][1]] = list_h[x]
        cv.imwrite(path_ic, new_img)


def size(in_height, in_width, in_list, g):
    x_min = round(in_width * (float(in_list[g][1]) - float(in_list[g][3]) / 2))
    x_max = round(in_width * (float(in_list[g][1]) + float(in_list[g][3]) / 2))
    y_min = round(in_height * (float(in_list[g][2]) - float(in_list[g][4]) / 2))
    y_max = round(in_height * (float(in_list[g][2]) + float(in_list[g][4]) / 2))
    return x_min, x_max, y_min, y_max


def doc(path, list_r, g_r):
    with open(path, 'r', encoding='utf-8', errors='ignore') as r:
        list_new = []
        while True:
            r_lines = r.readline()
            if not r_lines:
                break
            else:
                original_str = list_r[g_r][0] + ' ' + list_r[g_r][1] + ' ' + list_r[g_r][2] + ' ' + \
                               list_r[g_r][3] + ' ' + list_r[g_r][4] + '\n'
                if original_str == r_lines:
                    del r_lines
                else:
                    list_new.append(r_lines)
    with open(path, 'w', encoding='utf-8', errors='ignore') as w:
        w.writelines(list_new)


def main():
    if len(sys.argv) != 4:
        print('请依次输入<images>/<labels>路径，以及百分百大小<number>[0~100)')
        sys.exit(0)
    else:
        argv_1, argv_2, argv_3 = sys.argv[1], sys.argv[2], sys.argv[3]
        list_txt = os.listdir(argv_2)
        list_txt.sort()
        return argv_3, list_txt


def start():
    argv, list_t = main()
    num = input('请选择如何操作较小目标： 1 遮盖，2 删除框: ')
    if int(num) == 1:
        run(argv, list_t, amount=1)
    else:
        run(argv, list_t, amount=2)


if __name__ == '__main__':
    start()
