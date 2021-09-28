import shutil
import os
import time
import tqdm
from Images_labels_tools.function import public_function
from Images_labels_tools.config import setting


def lab_split(l_argv_1, l_argv_2, l_argv_3, l_time):
    for i in tqdm.tqdm(l_argv_1):
        i_split = os.path.split(i)[-1]
        l_list = []
        txt_list = public_function.read_txt(i)
        for j in txt_list:
            j_cls = j.split(' ')[0]
            if int(j_cls) in l_argv_3:
                l_list.append(j)
        if len(l_list) == 0:
            continue
        else:
            img_path, lab_path = mkdir_(l_argv_2, l_time)
            abs_img_path = os.path.join(img_path, i_split.replace('.txt', '.jpg', 1))
            abs_lab_path = os.path.join(lab_path, i_split)
            shutil.copy(i.replace('labels', 'images', 1).replace('.txt', '.jpg', 1), abs_img_path)
            public_function.write_txt(abs_lab_path, l_list)


def mkdir_(m_path, m_time):
    img_path = public_function.mkdir(m_path, m_time + '_split_images')
    lab_path = public_function.mkdir(m_path, m_time + '_split_labels')
    return img_path, lab_path


def start():
    argv_1 = public_function.Public().file_operate()
    argv_2 = public_function.Public().lab_path
    argv_3 = setting.labels_split['classes']
    time_s = time.localtime()
    time_ss = time.strftime("%Y_%m_%d_%H_%M_%S", time_s)
    lab_split(argv_1, argv_2, argv_3, time_ss)
