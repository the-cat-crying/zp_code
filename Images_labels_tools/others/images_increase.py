# -*- coding:utf-8 -*-
# 作者:周鹏
from PIL import Image, ImageDraw
import numpy as np
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
import os


def get_random_data(annotation_line, input_shape):
    """random preprocessing for real-time data augmentation"""
    h, w = input_shape
    min_offset_x = rand_2()
    min_offset_y = rand_2()
    scale_low = 1 - min(min_offset_x, min_offset_y)
    scale_high = scale_low + 0.2

    image_data_s = []
    box_data_s = []
    # index为了取place_x, place_y中的值
    index = 0
    # 确定四个图片存放的起点
    place_x = [0, 0, int(w * min_offset_x), int(w * min_offset_x)]
    place_y = [0, int(h * min_offset_y), int(w * min_offset_y), 0]
    for line_p in annotation_line:
        # 每一行进行分割
        line_content = line_p.strip('\n')
        # 打开图片
        image = Image.open(line_content)
        image = image.convert("RGB")
        iw, ih = image.size
        # 保存框的位置
        box = box_add(line_content, iw, ih)
        # 是否翻转图片
        image, box = picture_rotation(box, image, iw)
        # 对图片进行缩放
        image, nw, nh = zoom(image, w, h, scale_low, scale_high)
        # 进行色域变换
        image = color_change(image)
        # 将图片进行放置，分别对应四张分割图片的位置
        # x,y平移量
        dx = place_x[index]
        dy = place_y[index]
        # 创建一个三通道w, h的图片
        new_image = Image.new('RGB', (w, h), (128, 128, 128))
        # 把处理后的图片放在新创建图片的指定位置。
        new_image.paste(image, (dx, dy))
        images_data = np.array(new_image) / 255
        image_data_s.append(images_data)
        # 对box进行第一次处理
        box_data_s, b_data = box_deal_with(box, box_data_s, w, h, nw, nh, iw, ih, dx, dy)
        index = index + 1

    # 图片拼接
    new_image, cut_x, cut_y = splicing(w, h, min_offset_x, min_offset_y, image_data_s)
    # 对框进行进一步的处理
    new_boxes = merge_b_box(box_data_s, cut_x, cut_y)
    # 画框
    draw(new_image, new_boxes)


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
    path = os.path.join(os.path.dirname(path_l), 'labels_t', file_n.split('.')[0] + '.txt')
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
        # box = np.array([np.array(list(map(int, box.split(',')))) for box in line_content[1:]])
        # image.save(str(index)+".jpg")
    return box


def splicing(w, h, min_offset_x, min_offset_y, image_data_s):
    # 设置分割线x,y
    cut_x = np.random.randint(int(w * min_offset_x), int(w * (1 - min_offset_x)))
    cut_y = np.random.randint(int(h * min_offset_y), int(h * (1 - min_offset_y)))
    # 将图片分割，放在一起
    new_image = np.zeros([h, w, 3])
    new_image[:cut_y, :cut_x, :] = image_data_s[0][:cut_y, :cut_x, :]
    new_image[cut_y:, :cut_x, :] = image_data_s[1][cut_y:, :cut_x, :]
    new_image[cut_y:, cut_x:, :] = image_data_s[2][cut_y:, cut_x:, :]
    new_image[:cut_y, cut_x:, :] = image_data_s[3][:cut_y, cut_x:, :]

    img_s = Image.fromarray((new_image * 255).astype(np.uint8))
    img_s.show()
    return new_image, cut_x, cut_y


def draw(images_data, b_data):
    # 画框
    images_s = Image.fromarray((images_data * 255).astype(np.uint8))
    for k in range(len(b_data)):
        thickness = 2
        x_min, y_min, x_max, y_max = b_data[k][0:4]
        draw_s = ImageDraw.Draw(images_s)
        for i in range(thickness):
            # 画三次框使线条更宽
            draw_s.rectangle([x_min + i, y_min + i, x_max - i, y_max - i], outline=(255, 255, 255))
    images_s.show()


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
    image.show()
    return image


def box_deal_with(box, box_data_s, w, h, nw, nh, iw, ih, dx, dy):
    b_data = []
    # 对box进行重新处理
    if len(box) > 0:
        # np.random.shuffle(box)
        # 将x_min,x_max坐标先缩放再平移
        box[:, [0, 2]] = box[:, [0, 2]] * nw / iw + dx
        # 将y_min,y_max坐标先缩放再移动
        box[:, [1, 3]] = box[:, [1, 3]] * nh / ih + dy
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
        # 这两行可有可无
        b_data = np.zeros((len(box), 5))
        b_data[:len(box)] = box
        box_data_s.append(b_data)
    return box_data_s, b_data


def merge_b_box(img_box, cut_xx, cut_yy):
    merge_bbox = []
    for i in range(len(img_box)):
        for box in img_box[i]:
            x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
            # 第一张图
            if i == 0:
                # 本图片内框在分割线以外的舍弃
                if y1 > cut_yy or x1 > cut_xx:
                    continue
                if y2 >= cut_yy >= y1:
                    y2 = cut_yy
                    # 高度小于5个像素舍弃
                    if y2 - y1 < 5:
                        continue
                if x2 >= cut_xx >= x1:
                    x2 = cut_xx
                    # 宽度小于5个像素舍弃
                    if x2 - x1 < 5:
                        continue
            # 第二张图
            if i == 1:
                if y2 < cut_yy or x1 > cut_xx:
                    continue

                if y2 >= cut_yy >= y1:
                    y1 = cut_yy
                    if y2 - y1 < 5:
                        continue

                if x2 >= cut_xx >= x1:
                    x2 = cut_xx
                    if x2 - x1 < 5:
                        continue
            # 第三张图
            if i == 2:
                if y2 < cut_yy or x2 < cut_xx:
                    continue

                if y2 >= cut_yy >= y1:
                    y1 = cut_yy
                    if y2 - y1 < 5:
                        continue

                if x2 >= cut_xx >= x1:
                    x1 = cut_xx
                    if x2 - x1 < 5:
                        continue
            # 第四张图
            if i == 3:
                if y1 > cut_yy or x2 < cut_xx:
                    continue

                if y2 >= cut_yy >= y1:
                    y2 = cut_yy
                    if y2 - y1 < 5:
                        continue

                if x2 >= cut_xx >= x1:
                    x1 = cut_xx
                    if x2 - x1 < 5:
                        continue
            merge_bbox.append([x1, y1, x2, y2, box[-1]])
    return merge_bbox


if __name__ == "__main__":
    with open("/home/zhoup/work/yolomark/img/20200506_work/train.txt") as f:
        lines = f.readlines()
    a = np.random.randint(0, len(lines)-3)
    line = lines[a:a + 4]
    get_random_data(line, [618, 618])
