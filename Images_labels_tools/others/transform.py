import os
import cv2
import tqdm
import argparse
import threading
from multiprocessing import cpu_count


def parse_():
    parser = argparse.ArgumentParser(description='run a file move')
    parser.add_argument('--img', type=str, default='/home/gy/mount_sdc/from_testing_division/20210907_from_xwy_Y33_test_set/Y33_模拟识别/Y33_晴天')
    parser.add_argument('--save_lab', type=str, default='/home/gy/mount_sdc/from_testing_division/20210907_from_xwy_Y33_test_set/Y33_模拟识别/labels3')
    args = parser.parse_args()
    return args


def coord(c_a, c):
    b = os.listdir(c_a)
    b.sort()
    for i in tqdm.tqdm(b):
        list_ = []
        i_path = os.path.join(c_a, i)
        read = cv2.imread(i_path)
        o_h, o_w, _ = read.shape
        i_ = i.split('.')[0]
        i__ = i_.split('x')[0]
        width = int(i__)
        height = int(i_.split('x')[1].split('_')[0])
        x_min = int(i_.split('x')[1].split('_')[1])
        y_min = int(i_.split('x')[1].split('_')[2])
        x_center = x_min + width / 2
        y_center = y_min + height / 2
        x = round(x_center / o_w, 6)
        y = round(y_center / o_h, 6)
        w = round(width / o_w, 6)
        h = round(height / o_h, 6)
        list_.append(' '.join(['0', str(x), str(y), str(w), str(h) + '\n']))
        with open(os.path.join(c, i.replace('.jpg', '.txt', 1)), 'w', encoding='utf-8') as f:
            f.writelines(list_)


if __name__ == '__main__':
    args_ = parse_()
    index = cpu_count() / 2
    for i in range(0, int(index)):
        threading.Thread(target=coord, args=(args_.img, args_.save_lab)).start()
