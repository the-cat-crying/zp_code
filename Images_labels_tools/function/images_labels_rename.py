# -*- coding:utf-8 -*-
# 作者:周鹏
import os
import time
import shutil
from Images_labels_tools.function import public_function
from Images_labels_tools.config import setting


def new_mkdir_copy(n_time_str, path_3, path_4):
    # 时间返回一个可读形式为24个字符的字符串
    # now_time = time.asctime()
    # 获取上一层路径名创建新'backup_'文件夹路径
    path_dirname = os.path.dirname(path_3)
    path_join = os.path.join(path_dirname, 'backup_' + n_time_str, 'images')
    path_join_2 = os.path.join(path_dirname, 'backup_' + n_time_str, 'labels')
    # 创建多级目录
    os.makedirs(path_join)
    os.makedirs(path_join_2)

    for root, dirs, files in os.walk(path_3):
        for file in files:
            scr = os.path.join(path_3, file)
            shutil.copy(scr, path_join)

    for root_2, dirs_2, files_2 in os.walk(path_4):
        for file_2 in files_2:
            scr_2 = os.path.join(path_4, file_2)
            shutil.copy(scr_2, path_join_2)


def img_txt_contrast(argv_1, argv_2, argv_3, argv_4):
    x = os.listdir(argv_1)
    y = os.listdir(argv_2)
    delete(argv_3, argv_4, argv_1, x, '.jpg')
    delete(argv_3, argv_4, argv_2, y, '.txt')


def delete(argv_3, argv_4, argv, n, str_d):
    i = int(argv_3)
    for item in sorted(os.listdir(argv)):
        src = os.path.join(argv, item)
        poor = int(argv_4) - len(str(i))
        dst = os.path.join(argv, '0' * poor + str(i) + str_d)
        shutil.move(src, dst)

        print('\r对照重命名进度{:.2%}'.format((i - int(argv_3) + 1) / len(n)), end='')
        i = i + 1
    print()


def images_labels_rename_start():
    argv_1 = public_function.Public().img_path  # images路径
    argv_2 = public_function.Public().lab_path  # labels路径
    argv_3 = setting.dict_renames['start_number']
    argv_4 = setting.dict_renames['number_len']
    time_s = time.localtime()
    time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time_s)
    new_mkdir_copy(time_str, path_3=argv_1, path_4=argv_2)
    img_txt_contrast(argv_1, argv_2, argv_3, argv_4)
