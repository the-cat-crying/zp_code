import shutil
import os
import random
from Images_labels_tools.function import labels_operate
from Images_labels_tools.config import setting
from Images_labels_tools.function import public_function


def img_filter(i_argv_1, i_argv_2):
    i_set = labels_operate.txt_set(i_argv_1)
    cls_number = labels_operate.statistics(i_argv_1)
    dict_1 = {}
    for i in sorted(i_set):
        dict_1[i] = 0
    while True:
        if len(i_argv_1) == 0:
            break
        else:
            txt_s = random.sample(i_argv_1, 1)
            j = txt_s[0]
            set_1 = set()
            txt_list = public_function.read_txt(j)
            for k in txt_list:
                split_k = k.split(' ')[0]
                set_1.add(split_k)
            for u in set_1:
                if u in dict_1:
                    dict_1[u] += 1
            d_list = []
            for d in set_1:
                if dict_1[d] / cls_number[d] <= setting.images_test['scale']:
                    d_list.append(1)
                else:
                    d_list.append(0)
            if sum(d_list) == 0:
                i_argv_1.remove(j)
            else:
                lab_path, img_path = mkdir_(i_argv_2)
                abs_lab_path = os.path.join(lab_path, j.split('/')[-1])
                abs_img_path = os.path.join(img_path, j.split('/')[-1].replace('.txt', '.jpg', 1))
                old_img_path = j.replace('labels', 'images', 1)
                old_img_path = old_img_path.replace('.txt', '.jpg', 1)
                shutil.move(j, abs_lab_path)
                shutil.move(old_img_path, abs_img_path)
                i_argv_1.remove(j)


def mkdir_(m_argv_2):
    lab_path = public_function.mkdir(m_argv_2, 'test_labels')
    img_path = public_function.mkdir(m_argv_2, 'test_images')
    return lab_path, img_path


def start():
    argv_1 = public_function.Public().file_operate()
    argv_2 = public_function.Public().lab_path
    img_filter(argv_1, argv_2)
