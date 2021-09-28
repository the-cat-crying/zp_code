import os
import tqdm
import shutil
import argparse


def parse_():
    parser = argparse.ArgumentParser(description='run a file move')
    parser.add_argument('-img', '--images', type=str, default='')
    parser.add_argument('-lab', '--labels', type=str, default='')
    parser.add_argument('-lab_img', type=str, default=True, help='labels move to images')
    parser.add_argument('-img_lab', type=str, default=False, help='images move to labels')
    args = parser.parse_args()
    return args


def move(m_p_img, m_p_lab, m_lab_img, m_img_lab):
    if m_lab_img:
        list_lab = os.listdir(m_p_lab)
        list_lab.sort()
        for index in tqdm.tqdm(list_lab):
            abs_lab = os.path.join(m_p_lab, index)
            abs_lab_img = abs_lab.replace('labels', 'images', 1)
            shutil.move(abs_lab, abs_lab_img)
    if m_img_lab:
        list_img = os.listdir(m_p_img)
        list_img.sort()
        for index2 in tqdm.tqdm(list_img):
            if index2.split('.')[-1] == 'txt':
                abs_img = os.path.join(m_p_img, index2)
                abs_img_lab = abs_img.replace('images', 'labels', 1)
                shutil.move(abs_img, abs_img_lab)


if __name__ == '__main__':
    args_ = parse_()
    move(args_.img, args_.lab, args_.lab_img, args_.img_lab)
