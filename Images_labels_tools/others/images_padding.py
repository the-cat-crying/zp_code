import os
import threading
import tqdm
import cv2
from multiprocessing import cpu_count
import argparse


def parser():
    # 填写路径
    parser_ = argparse.ArgumentParser(description="YOLO Object Detection")
    parser_.add_argument("--raw_img", type=str,
                         default="/home/gy/mount_sdc/from_testing_division/20210907_from_xwy_Y33_test_set/Y33_模拟识别/test5_small.txt",
                         help="input raw images path")
    parser_.add_argument("--raw_lab", type=str,
                         default="/home/gy/mount_sdc/from_testing_division/20210907_from_xwy_Y33_test_set/Y33_模拟识别/Y33_高对比度_labels",
                         help="input raw labels path")
    parser_.add_argument("--save_lab", type=str,
                         default="/home/gy/mount_sdc/from_testing_division/20210907_from_xwy_Y33_test_set/Y33_模拟识别/Y33_高对比度_small",
                         help="save new labels path")
    parser_.add_argument("--save_img",
                         default="./work/20210913_EfficientNet_12358_migrate/data",
                         help="save new images path")
    parser_.add_argument("--width", type=int, default=320, help="output width")
    parser_.add_argument("--height", type=int, default=320, help="output height")
    return parser_.parse_args()


def surplus(n_height, n_width, height, width, img):
    surplus_h = n_height - height
    surplus_w = n_width - width
    top = int(surplus_h / 2)
    bottom = surplus_h - top
    left = int(surplus_w / 2)
    right = surplus_w - left
    scale_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    return scale_img, top, bottom, left, right


def write(w_lab_path, w_lab_save, w_left, w_top, w_old_w, w_old_h, w_new_w, w_new_h, w_scale_end):
    with open(w_lab_path, 'r', encoding='utf-8') as file:
        file_list = file.readlines()
        new_all = []
        for index2 in file_list:
            index_split = index2.strip('\n').split(' ')
            x_center = float(index_split[1]) * w_old_w * w_scale_end
            y_center = float(index_split[2]) * w_old_h * w_scale_end
            width = float(index_split[3]) * w_old_w * w_scale_end
            height = float(index_split[4]) * w_old_h * w_scale_end
            new_x_min = int(x_center - width / 2) + w_left
            new_x_max = int(x_center + width / 2) + w_left
            new_y_min = int(y_center - height / 2) + w_top
            new_y_max = int(y_center + height / 2) + w_top
            new_x_center = round((new_x_min + (new_x_max - new_x_min) / 2) / w_new_w, 6)
            new_y_center = round((new_y_min + (new_y_max - new_y_min) / 2) / w_new_h, 6)
            new_width = round((new_x_max - new_x_min) / w_new_w, 6)
            new_height = round((new_y_max - new_y_min) / w_new_h, 6)
            coord = list(map(str, [index_split[0], new_x_center, new_y_center, new_width, new_height]))
            new_coord = ' '.join(coord) + '\n'
            new_all.append(new_coord)
        with open(w_lab_save, 'w', encoding='utf-8') as f:
            f.writelines(new_all)


class Pad(object):
    def __init__(self, new_height, new_width, raw_lab_path, raw_img_path, lab_save, img_save):
        self.new_height = new_height
        self.new_width = new_width
        self.raw_lab_path = raw_lab_path
        self.raw_img_path = raw_img_path
        self.lab_save = lab_save
        self.img_save = img_save

    def padding(self):
        img_list = os.listdir(self.raw_img_path)
        img_list.sort()
        for index1 in tqdm.tqdm(img_list, desc='read_img'):
            trans = index1.replace('.jpg', '.txt', 1)
            abs_img_path = os.path.join(self.raw_img_path, index1)
            abs_lab_path = os.path.join(self.raw_lab_path, trans)

            abs_save_lab = os.path.join(self.lab_save, trans)
            abs_save_img = os.path.join(self.img_save, index1)
            images = cv2.imread(abs_img_path)
            old_height, old_width, old_channel = images.shape
            if old_height <= self.new_height and old_width <= self.new_width:
                images, top, bottom, left, right = surplus(self.new_height, self.new_width,
                                                           old_height, old_width, images)
                scale_end = 1
                write(abs_lab_path, abs_save_lab, left, top, old_width, old_height, self.new_width, self.new_height,
                      scale_end)
                cv2.imwrite(abs_save_img, images)
            else:
                scale_h = self.new_height / old_height
                scale_w = self.new_width / old_width
                scale_end = min(scale_h, scale_w)
                scale_img = cv2.resize(images, None, fx=scale_end, fy=scale_end, interpolation=cv2.INTER_AREA)
                scale_height, scale_width, _ = scale_img.shape
                scale_img, top, bottom, left, right = surplus(self.new_height, self.new_width, scale_height,
                                                              scale_width, scale_img)
                write(abs_lab_path, abs_save_lab, left, top, old_width, old_height, self.new_width, self.new_height,
                      scale_end)
                cv2.imwrite(abs_save_img, scale_img)


if __name__ == '__main__':
    args = parser()
    t1 = Pad(args.height, args.width, args.raw_lab, args.raw_img, args.save_lab, args.save_img)
    index = cpu_count() / 2
    for i in range(0, int(index)):
        threading.Thread(target=t1.padding, args=()).start()
