# -*- coding:utf-8 -*-
# 作者:周鹏
import argparse


# images/labels路径
# dict_data = {
#     'images_path': '%s/%s' % (path, 'data/images'),
#     'labels_path': '%s/%s' % (path, 'data/labels')
# }
dict_data = {
    'images_path': '/home/gy/mount_sdc/work_zp/dataset/train-data/from_coco_3cls_add_4cls_all_7classes_320_320/images',
    'labels_path': '/home/gy/mount_sdc/work_zp/dataset/train-data/from_coco_3cls_add_4cls_all_7classes_320_320/labels'
}

# 图片重命名
# 输入数字大于images总数长度(如123张，输入数字为4),决定有多少位数
# 起始数字
dict_rename = {
    'images_renames': False,
    'start_number': 5,
    'images_len': 6
}

# 标签统计，去重, w/h=0-remove,和标签对照删除，标注框是否超出图片边界检验
labels_operate = {
    'labels_operate': False
}

# labels类别筛选，classes位保留的类别
labels_split = {
    'labels_classes_split': False,
    'classes': [0, 2, 4]
}

# labels_file_replace，标签追加，替换，类别替换
labels_replace = {
    'labels_file_replace': False,
    'lab_add': '8 0.298047 0.293750 0.182031 0.095833\n',
    'lab_rep_old': '8 0.298047 0.293750 0.182031 0.095833\n',
    'lab_rep_new': '8 0.323828 0.282639 0.182031 0.095833\n'
}

# 图片和标签对照重命名
# 输入数字大于images总数长度(如123张，输入数字为4),决定有多少位数
# 起始数字
dict_renames = {
    'images_labels_renames': False,
    'start_number': 14134,
    'number_len': 6
}

# 遮盖，需要输入类别
dict_cover = {
    'images_covers': False,
    'category': 1
}

# 测试图片筛选, scale占图片的百分之几
images_test = {
    'images_test_filter': False,
    'scale': 0.1
}


# video_copy_padding视频填充, 宽高要大于原视频宽高，视频保存为视频或者图片，图片保存为视频或者图片，设置args参数
def make_parser():
    parser = argparse.ArgumentParser("Demo!")
    parser.add_argument('-demo', default='images', help='demo read images, video')
    parser.add_argument('-save', default='vid', help='demo save img, vid')
    return parser


args = make_parser().parse_args()

video_copy_padding = {
    'video_copy_padding': False,
    'out_width': 1920,
    'out_height': 1080
}

# mosaic,value为一组值
mosaic = {
    'mosaic': False,
    'value': [960, 960]
}

# cutout随机类别mask
cutout = {
    'cutout': False
}

# cut_mix两张图片融合
cut_mix = {
    'cut_mix': False
}
