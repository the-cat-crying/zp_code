# -*- coding:utf-8 -*-
# 作者:周鹏
from Images_spin.func import function
from Images_spin.func import func_images
import argparse


def run():
    parser = argparse.ArgumentParser(description="Demo of argparse")
    parser.add_argument('-i', '--images', default='images_labels')
    args = parser.parse_args()
    name = args.images
    if name == 'images':
        func_images.img_aug.process_img()
    else:
        function.img_aug.process_img()
