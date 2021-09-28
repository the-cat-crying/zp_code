import tqdm
import os
import sys
import cv2 as cv
from Images_labels_tools.function import public_function


# labels标签去重
def deduplication(path_dir):
    # 集合（set）是一个无序的不重复元素序列
    for i in tqdm.tqdm(path_dir, desc='标签去重'):
        set_all = set()
        file_list = public_function.read_txt(i)
        set_all.update(file_list)
        public_function.write_txt(i, list(set_all))


# 去除高和宽为0的情况
def remove_zero(r_txt_path):
    zeros = ['0', '0.0', '0.00', '0.000', '0.0000', '0.00000', '0.000000', '0.0000000']

    for i in tqdm.tqdm(r_txt_path, desc='去高宽为0'):
        new_list = []
        file_list = public_function.read_txt(i)
        for j in file_list:
            index_ = j.strip('\n').split(' ')
            if index_[3] in zeros or index_[4] in zeros:
                continue
            else:
                new_list.append(j)
        public_function.write_txt(i, new_list)


# 标签类别统计
def statistics(s_txt_list):
    set_s = txt_set(s_txt_list)
    dict_s = {}
    dict_ss = {}
    for o in set_s:
        dict_s[o] = 0
        dict_ss[o] = 0
    for i in tqdm.tqdm(s_txt_list, desc='类别统计'):
        file_list = public_function.read_txt(i)
        set_ss = set()
        for j in file_list:
            index = j.split(' ')[0]
            if index in dict_s:
                set_ss.add(index)
                dict_s[index] += 1
        for k in set_ss:
            if k in dict_ss:
                dict_ss[k] += 1
    for x in sorted(dict_s):
        print('{0}_类类别个数为: {1:6d}    {0}_类总图片数量: {2}'.format(x, dict_s[x], dict_ss[x]))
    return dict_ss


def txt_set(t_txt_path):
    set_s = set()
    for i in tqdm.tqdm(t_txt_path, desc='make-set'):
        file_list = public_function.read_txt(i)
        for j in file_list:
            set_s.add(j.split(' ')[0])
    return set_s


# images和labels对照删除
def file_re(path_1):
    for index in path_1:
        prefix, suffix = os.path.split(index)
        if suffix.split('.')[1] == 'txt':
            print("images中有txt文件。")
            sys.exit()


def dict_file(list_path):
    dict_all = {}
    for index in list_path:
        size_file = os.path.getsize(index)
        prefix, suffix = os.path.split(index)
        suffix_split = suffix.split('.')
        matrix = os.path.join(prefix.rstrip('/'), suffix_split[0])
        dict_all[matrix] = size_file
    return dict_all


def dict_delete(d_img_dict, d_lab_dict, d_img_path, d_lab_path, d_num):
    number = 0
    list_ = []
    if d_num == 1:
        for key, index in d_lab_dict.items():
            if index == 0:
                os.remove('.'.join([key, 'txt']))
                list_.append(key)
                number += 1
        for value in list_:
            del d_lab_dict[value]

    times = 0
    for key_img in d_img_dict:
        prefix, suffix = os.path.split(key_img)
        key_lab = os.path.join(d_lab_path, suffix)
        if key_lab not in d_lab_dict:
            key_path = '.'.join([key_img, 'jpg'])
            os.remove(key_path)
            times = times + 1

    times_s = 0
    for key_labels in d_lab_dict:
        prefix_, suffix_ = os.path.split(key_labels)
        key_images = os.path.join(d_img_path, suffix_)
        if key_images not in d_img_dict:
            key_path = '.'.join([key_labels, 'txt'])
            os.remove(key_path)
            times_s = times_s + 1
    print("删除0KB、txt数目: {}".format(number))
    print("删除images数目: {}".format(times))
    print("删除labels数目: {}".format(times_s))
    print("剩余images数目: {0}".format(len(os.listdir(d_img_path))))
    print("剩余labels数目: {0}".format(len(os.listdir(d_lab_path))))
    print()


# 标注框是否超出图片边界检验
def coord(labels_list, argv_img):
    for i in tqdm.tqdm(labels_list, '边界检测'):
        list_all = []
        _, index = os.path.split(i)
        image_txt = os.path.join(argv_img, index.split('.')[0] + '.jpg')
        img_read = cv.imread(image_txt)
        height, width = img_read.shape[0], img_read.shape[1]
        with open(i, 'r', encoding='utf-8', errors='ignore') as f:
            while True:
                f_line = f.readline()
                if not f_line:
                    break
                else:
                    # 防止没有超出多次计算造成误差
                    instance = False
                    line = f_line.strip('\n').split(' ')
                    cls, x_min, y_min, x_max, y_max = public_function.coordinate(line, height, width)
                    if x_min < 0:
                        x_max = x_max + abs(x_min)
                        x_min = 0
                        instance = True
                    if y_min < 0:
                        y_max = y_max + abs(y_min)
                        y_min = 0
                        instance = True
                    if x_max > width:
                        x_min = x_min - (x_max - width)
                        x_max = width
                        instance = True
                    if y_max > height:
                        y_min = y_min - (y_max - height)
                        y_max = height
                        instance = True
                    if instance:
                        coord_str = public_function.str_coord(cls, x_min, y_min, x_max, y_max, height, width)
                        list_all.append(coord_str)
                    else:
                        list_all.append(f_line)
        public_function.write_txt(i, list_all)


def start():
    labels_path_all = public_function.Public().file_operate()
    images_path_all = public_function.Public().picture_operate()
    img_path = public_function.Public().img_path
    lab_path = public_function.Public().lab_path

    # 标签去重
    deduplication(labels_path_all)

    # width and height == 0 remove
    remove_zero(labels_path_all)

    # sys.argv[1] == images, sys.argv[2] == labels
    # images和labels对照删除
    file_re(images_path_all)
    num_1 = int(input("请输入(1:删除 2:保留)0KB文件: "))
    img_dict = dict_file(images_path_all)
    lab_dict = dict_file(labels_path_all)
    dict_delete(img_dict, lab_dict, img_path, lab_path, num_1)

    lab_list = public_function.Public().file_operate()

    # 标签类别统计
    statistics(lab_list)

    # 标注框是否超出图片边界检验
    sure = input('是否进行边界检测(yes or no): ')
    if sure == 'yes':
        coord(lab_list, img_path)
