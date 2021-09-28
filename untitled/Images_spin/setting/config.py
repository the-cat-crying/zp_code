# -*- coding:utf-8 -*-
# 作者:周鹏
import os
import sys
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(sys_path)

Date = {
    "img_path": "%s/%s" % (sys_path, "images_labels/images"),
    "crate_i": "%s/%s" % (sys_path, "images_labels/new_images/"),
    "tables_path": "%s/%s" % (sys_path, "images_labels/labels"),
    "crate_t": "%s/%s" % (sys_path, "images_labels/new_labels/"),
    "spin_degree": [60, 80, 90, 100, 160],
    "scale": 1.
}
