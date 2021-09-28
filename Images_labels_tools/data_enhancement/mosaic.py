# -*- coding:utf-8 -*-
# 作者:周鹏
import random
from PIL import Image
import numpy as np
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
import os
from Images_labels_tools.function import public_function
from Images_labels_tools.config import setting


def get_random_data(annotation_line, input_shape, g_argv_2, g_number):
    """random preprocessing for real-time data augmentation"""
    h, w = input_shape
    min_offset_x = rand_2()
    min_offset_y = rand_2()
    scale_low = 1 - min(min_offset_x, min_offset_y)
    scale_high = scale_low + 0.2

    # index为了取place_x, place_y中的值
    index = 0
    cut_x = np.random.randint(int(w * min_offset_x), int(w * (1 - min_offset_x)))
    cut_y = np.random.randint(int(h * min_offset_y), int(h * (1 - min_offset_y)))
    # 创建一个三通道w, h的图片
    new_image = Image.new('RGB', (w, h), (128, 128, 128))
    new_image = np.array(new_image)
    tt_list = []
    for line_p in annotation_line:
        # 打开图片
        image = Image.open(line_p)
        image = image.convert("RGB")
        iw, ih = image.size
        # 保存框的位置
        box = box_add(line_p, iw, ih)
        # 是否翻转图片
        image, box = picture_rotation(box, image, iw)
        # 对图片进行缩放
        image, nw, nh = zoom(image, w, h, scale_low, scale_high)
        # 进行色域变换
        # 对box进行第一次处理
        b_data = box_deal_with(box, w, h, nw, nh, iw, ih)
        image = color_change(image)
        image = np.array(image)

        if index == 0:
            new_image, y_min, y_max, x_min, x_max = img_with(nw, nh, cut_x, cut_y, 0, cut_y, 0, cut_x, image, new_image)
            tt_list = merge_b_box(b_data, cut_x, cut_y, index, y_min, y_max, x_min, x_max, w, h, tt_list)
        if index == 1:
            new_image, y_min, y_max, x_min, x_max = img_with(nw, nh, cut_x, (h - cut_y), cut_y, h, 0, cut_x, image, new_image)
            tt_list = merge_b_box(b_data, cut_x, cut_y, index, y_min, y_max, x_min, x_max, w, h, tt_list)
        if index == 2:
            new_image, y_min, y_max, x_min, x_max = img_with(nw, nh, (w - cut_x), (h - cut_y), cut_y, h, cut_x, w, image, new_image)
            tt_list = merge_b_box(b_data, cut_x, cut_y, index, y_min, y_max, x_min, x_max, w, h, tt_list)
        if index == 3:
            new_image, y_min, y_max, x_min, x_max = img_with(nw, nh, (w - cut_x), cut_y, 0, cut_y, cut_x, w, image, new_image)
            tt_list = merge_b_box(b_data, cut_x, cut_y, index, y_min, y_max, x_min, x_max, w, h, tt_list)

        index = index + 1
    img_path = public_function.mkdir(g_argv_2, 'mosaic_images')
    lab_path = public_function.mkdir(g_argv_2, 'mosaic_labels')
    abs_img_path = os.path.join(img_path, str(g_number) + '.jpg')
    abs_lab_path = os.path.join(lab_path, str(g_number) + '.txt')
    public_function.write_txt(abs_lab_path, tt_list)
    images_s = Image.fromarray(new_image.astype(np.uint8))
    images_s.save(abs_img_path)
    # images_s.show()


def img_with(i_nw, i_nh, i_cut_x, i_cut_y, y_, y_m, x_, x_m, i_image, i_new_image):
    while True:
        x_min = random.randint(0, i_nw // 2)
        y_min = random.randint(0, i_nh // 2)
        x_max = x_min + i_cut_x
        y_max = y_min + i_cut_y
        if x_max <= i_nw and y_max <= i_nh:
            i_new_image[y_:y_m, x_:x_m] = i_image[y_min:y_max, x_min:x_max]
            break
    return i_new_image, y_min, y_max, x_min, x_max


def rand(h=0.0, b=1.0):
    # np.random.rand() 生成[0, 1)随机数
    x = np.random.rand() * (b - h) + h
    return x


def rand_2():
    average = 0
    while 0.2 > average or average > 0.5:
        average = np.random.rand()
    return average


def box_add(line_content, iw, ih):
    path_l, file_n = os.path.split(line_content)
    path = os.path.join(os.path.dirname(path_l), 'labels', file_n.split('.')[0] + '.txt')
    with open(path, 'r', encoding='utf-8') as file:
        # 将x_min,y_min,x_max,y_max以列表的方式保存为矩阵，保存框的位置
        # ['263,211,324,339,8', '165,264,253,372,8', '241,194,295,299,8']
        list_all = []
        for box in file:
            cls_c, x_c, y_c, w_c, h_c = box.split(' ')[0], box.split(' ')[1], box.split(' ')[2], box.split(' ')[3],\
                                        box.strip('\n').split(' ')[4]
            x_min = (float(x_c) - float(w_c) / 2) * iw
            y_min = (float(y_c) - float(h_c) / 2) * ih
            x_max = (float(x_c) + float(w_c) / 2) * iw
            y_max = (float(y_c) + float(h_c) / 2) * ih
            x = list(map(int, [x_min, y_min, x_max, y_max, cls_c]))
            list_all.append(np.array(x))
        box = np.array(list_all)
    return box


def picture_rotation(box, image, iw):
    # 是否翻转图片
    flip = rand() < .5
    # image.show()
    if flip and len(box) > 0:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        # print(box[:, [0, 2]] ,box[:, [2, 0]])
        box[:, [0, 2]] = iw - box[:, [2, 0]]
        # image.show()
    return image, box


def zoom(image, w, h, scale_low, scale_high):
    # 对输入进来的图片进行缩放
    new_ar = w / h
    scale = rand(scale_low, scale_high)
    if new_ar < 1:
        nh = int(scale * h)
        nw = int(nh * new_ar)
        # image.show()
    else:
        nw = int(scale * w)
        nh = int(nw / new_ar)

    image = image.resize((nw, nh), Image.BICUBIC)
    # image.show()
    return image, nw, nh


def color_change(image, hue=.1, sat=1.5, val=1.5):
    # 进行色域变换
    hue = rand(-hue, hue)
    sat = rand(1, sat) if rand() < .5 else 1 / rand(1, sat)
    val = rand(1, val) if rand() < .5 else 1 / rand(1, val)
    x = rgb_to_hsv(np.array(image) / 255.)
    x[..., 0] += hue
    x[..., 0][x[..., 0] > 1] -= 1
    x[..., 0][x[..., 0] < 0] += 1
    x[..., 1] *= sat
    x[..., 2] *= val
    x[x > 1] = 1
    x[x < 0] = 0
    image = hsv_to_rgb(x)
    # Image.fromarray数组与image之间的转换
    image = Image.fromarray((image * 255).astype(np.uint8))
    # image.show()
    return image


def box_deal_with(box, w, h, nw, nh, iw, ih):
    # 对box进行重新处理
    if len(box) > 0:
        # np.random.shuffle(box)
        # 将x_min,x_max坐标先缩放再平移
        box[:, [0, 2]] = box[:, [0, 2]] * nw / iw
        # 将y_min,y_max坐标先缩放再移动
        box[:, [1, 3]] = box[:, [1, 3]] * nh / ih
        # 选出x_min,y_min超出图片部分，将它修正
        box[:, 0:2][box[:, 0:2] < 0] = 0
        # 选出x_max,y_max超出图片部分，将它修正
        box[:, 2][box[:, 2] > w] = w
        box[:, 3][box[:, 3] > h] = h
        # 缩放移动后bbox的宽度和高度是否存在
        box_w = box[:, 2] - box[:, 0]
        box_h = box[:, 3] - box[:, 1]
        # >>> np.logical_and([True, False], [False, False])
        # array([False, False], dtype=bool)
        # 删除矩阵中w,h小于等于0的数据
        box = box[np.logical_and(box_w > 1, box_h > 1)]
    return box


def merge_b_box(img_box, cut_xx, cut_yy, m_index, m_y_min, m_y_max, m_x_min, m_x_max, m_w, m_h, m_list):
    for box in img_box:
        x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
        cls = int(box[-1])
        if x2 <= m_x_min or x1 >= m_x_max or y2 <= m_y_min or y1 >= m_y_max:
            continue
        else:
            x_min = np.clip(x1, m_x_min, m_x_max)
            x_max = np.clip(x2, m_x_min, m_x_max)
            y_min = np.clip(y1, m_y_min, m_y_max)
            y_max = np.clip(y2, m_y_min, m_y_max)
        # 第一张图
        if m_index == 0:
            x_min, x_max, y_min, y_max = crd(x_min, x_max, y_min, y_max, m_x_min, m_y_min, 0, 0)
            value1 = y_max - y_min
            value2 = x_max - x_min
            # 本图片内框在分割线以外的舍弃
            if value1 * value2 <= 25 or value1 <= 5 or value2 <= 5:
                continue
            txt_str = public_function.str_coord(cls, x_min, y_min, x_max, y_max, m_h, m_w)
            m_list.append(txt_str)
        # 第二张图
        if m_index == 1:
            x_min, x_max, y_min, y_max = crd(x_min, x_max, y_min, y_max, m_x_min, m_y_min, 0, cut_yy)
            value1 = y_max - y_min
            value2 = x_max - x_min
            # 本图片内框在分割线以外的舍弃
            if value1 * value2 <= 25 or value1 <= 5 or value2 <= 5:
                continue
            txt_str = public_function.str_coord(cls, x_min, y_min, x_max, y_max, m_h, m_w)
            m_list.append(txt_str)
        # 第三张图
        if m_index == 2:
            x_min, x_max, y_min, y_max = crd(x_min, x_max, y_min, y_max, m_x_min, m_y_min, cut_xx, cut_yy)
            value1 = y_max - y_min
            value2 = x_max - x_min
            # 本图片内框在分割线以外的舍弃
            if value1 * value2 <= 25 or value1 <= 5 or value2 <= 5:
                continue
            txt_str = public_function.str_coord(cls, x_min, y_min, x_max, y_max, m_h, m_w)
            m_list.append(txt_str)
        # 第四张图
        if m_index == 3:
            x_min, x_max, y_min, y_max = crd(x_min, x_max, y_min, y_max, m_x_min, m_y_min, cut_xx, 0)
            value1 = y_max - y_min
            value2 = x_max - x_min
            # 本图片内框在分割线以外的舍弃
            if value1 * value2 <= 25 or value1 <= 5 or value2 <= 5:
                continue
            txt_str = public_function.str_coord(cls, x_min, y_min, x_max, y_max, m_h, m_w)
            m_list.append(txt_str)
    return m_list


def crd(x_min, x_max, y_min, y_max, m_x_min, m_y_min, cut_xx, cut_yy):
    x_min = x_min - m_x_min + cut_xx
    x_max = x_max - m_x_min + cut_xx
    y_min = y_min - m_y_min + cut_yy
    y_max = y_max - m_y_min + cut_yy
    return x_min, x_max, y_min, y_max


def start():
    argv_1 = public_function.Public().picture_operate()
    argv_2 = public_function.Public().img_path
    argv_3 = setting.mosaic['value']
    index = os.listdir(argv_2)
    number = 0
    while True:
        if len(argv_1) == 0 or len(argv_1) == 1 or len(argv_1) == 2 or len(argv_1) == 3:
            break
        else:
            line = random.sample(argv_1, 4)
            get_random_data(line, argv_3, argv_2, number)
            argv_1.remove(line[0])
            argv_1.remove(line[1])
            argv_1.remove(line[2])
            argv_1.remove(line[3])
            number += 4
            print('\rmosaic增强进度: {0:.2%}'.format(number / len(index)), end='')
