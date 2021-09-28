import os
import json
import cv2
import argparse
from tqdm import tqdm


def parser():
    # 填写路径
    parser_ = argparse.ArgumentParser(description="YOLO Object Detection")
    parser_.add_argument("--input", type=str,
                         default="/home/gy/mount_sdc/from_testing_division/20210907_from_xwy_Y33_test_set/Y33_模拟识别/Y33_复杂光照.txt",
                         help="input dataset path")
    parser_.add_argument("--raw_lab", type=str,
                         default="/home/gy/mount_sdc/from_testing_division/20210907_from_xwy_Y33_test_set/Y33_模拟识别/Y33_复杂光照_all_labels",
                         help="input raw labels path")
    parser_.add_argument("--raw_img", type=str,
                         default="/home/gy/mount_sdc/from_testing_division/20210907_from_xwy_Y33_test_set/Y33_模拟识别/Y33_复杂光照",
                         help="input raw images path")
    parser_.add_argument("--data_file",
                         default="./work/20210922_EfficientNet_12358_migrate_four_anchors/data",
                         help="path to data file")
    parser_.add_argument("--config_file",
                         default="./work/20210922_EfficientNet_12358_migrate_four_anchors/yolo-2.7-xl.cfg",
                         help="path to config file")
    parser_.add_argument("--weights",
                         default="./work/20210922_EfficientNet_12358_migrate_four_anchors/yolo-2_best.weights",
                         help="yolo weights path")
    parser_.add_argument("--out_json", type=str,
                         default="./work/20210922_EfficientNet_12358_migrate_four_anchors/Y33_复杂光照.json",
                         help="labels save")
    parser_.add_argument("--convert_txt", type=str,
                         default="./work/20210922_EfficientNet_12358_migrate_four_anchors/result",
                         help="labels save txt file")
    parser_.add_argument("--thresh", type=float,
                         default=0.2,
                         help="Confidence")
    parser_.add_argument("--iou_thresh", type=float,
                         default=0.1,
                         help="mAP threshold")
    return parser_.parse_args()


def darknet(d_data, d_cfg, d_weight, d_save_json, d_input, d_convert_txt, d_thresh, d_raw_lab, d_iou_thresh):
    yolo_path = '/home/gy/mount_sdc/work_zp/Train/darknet-210902'
    os.system("cd {0} && ./darknet detector test {1} {2} {3} -thresh {4} -ext_output -dont_show "
              "-out {5} < {6}".format(yolo_path, d_data, d_cfg, d_weight, d_thresh, d_save_json, d_input))
    print()
    d_save_json = yolo_path + d_save_json.replace('./', '/')
    d_convert_txt = yolo_path + d_convert_txt.replace('./', '/')
    # 将json文件写入对应的txt文件中
    read_json(d_save_json, d_convert_txt)
    # 精确率和召回率计算
    calculate(d_raw_lab, d_convert_txt, d_iou_thresh)
    # delete result down all
    os.system("rm {}".format(d_convert_txt + "/*"))
    # 空类别图片测试
    # read_json_2(d_save_json)


def judgment(j_center_x, j_center_y, j_width, j_height, j_img_width, j_img_height):
    x_min = int((j_center_x - j_width / 2) * j_img_width)
    x_max = int((j_center_x + j_width / 2) * j_img_width)
    y_min = int((j_center_y - j_height / 2) * j_img_height)
    y_max = int((j_center_y + j_height / 2) * j_img_height)
    x_min = max(0, x_min)
    y_min = max(0, y_min)
    str_list = list(map(str, [x_min, y_min, x_max, y_max]))
    str_list = ' '.join(str_list) + '\n'
    return str_list


def read_json(r_argv_save_json, r_convert_txt):
    with open(r_argv_save_json, 'r', encoding='utf-8') as json_file:
        json_list = json.load(json_file, encoding='utf-8')
        for dict_J in tqdm(json_list, desc='json_input'):
            all_list = []
            img_data = dict_J["objects"]
            img_path = dict_J["filename"]
            img = cv2.imread(dict_J['filename'])
            img_height, img_width, img_channel = img.shape
            prefix, suffix = os.path.split(img_path)
            txt_save_path = os.path.join(r_convert_txt, suffix.replace('.jpg', '.txt'))
            if len(img_data) == 0:
                with open(txt_save_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write('')
            else:
                bad_cls = [2]
                for index in img_data:
                    class_id = index["class_id"]
                    confidence = index["confidence"]
                    relative = index['relative_coordinates']
                    center_x = float(relative['center_x'])
                    center_y = float(relative['center_y'])
                    width = float(relative['width'])
                    height = float(relative['height'])
                    area_ = int(width * img_width * height * img_height)
                    if class_id in bad_cls and area_ < 300:
                        if confidence > 0.8:
                            str_list = judgment(center_x, center_y, width, height, img_width, img_height)
                            all_list.append(str_list)
                    else:
                        str_list = judgment(center_x, center_y, width, height, img_width, img_height)
                        all_list.append(str_list)
                with open(txt_save_path, 'w', encoding='utf-8') as ff:
                    ff.writelines(all_list)


def calculate(c_raw_lab, c_result, c_iou_thresh):
    listdir_c = os.listdir(c_raw_lab)
    listdir_c.sort()
    list_TP = []
    list_FP = []
    list_FN = []
    for index_l in tqdm(listdir_c, desc='iou_calculate'):
        txt_path = os.path.join(c_raw_lab, index_l)
        prefix_img, suffix_img = os.path.split(args.raw_img)
        prefix_lab, suffix_lab = os.path.split(c_raw_lab)
        img_path = txt_path.replace(suffix_lab, suffix_img, 1)
        img_path_ = img_path.replace('.txt', '.jpg', 1)
        img = cv2.imread(img_path_)
        height, width, ch = img.shape
        raw_list = []
        cube_list = []
        with open(txt_path, 'r', encoding='utf-8') as f:
            f_o = f.readlines()
            for j in f_o:
                j_ = j.strip('\n').split(' ')
                x_min = int((float(j_[1]) - float(j_[3]) / 2) * width)
                x_max = int((float(j_[1]) + float(j_[3]) / 2) * width)
                y_min = int((float(j_[2]) - float(j_[4]) / 2) * height)
                y_max = int((float(j_[2]) + float(j_[4]) / 2) * height)
                raw_list.append([x_min, y_min, x_max, y_max])

        detector_path = os.path.join(c_result, index_l)
        with open(detector_path, 'r', encoding='utf-8') as f_:
            f_list = f_.readlines()
            for k in f_list:
                k_ = k.strip('\n').split(' ')
                x_k_min, y_k_min, x_k_max, y_k_max = int(k_[0]), int(k_[1]), int(k_[2]), int(k_[3])
                cube_list.append([x_k_min, y_k_min, x_k_max, y_k_max])

        for index in raw_list:
            xx_min, yy_min, xx_max, yy_max = index[0], index[1], index[2], index[3]
            remain = []
            extend_TP = []
            extend_FN = []
            for index_c in cube_list:
                # iou确定
                xk_min, yk_min, xk_max, yk_max = index_c[0], index_c[1], index_c[2], index_c[3]
                value_w = min(xk_max, xx_max) - max(xk_min, xx_min)
                value_h = min(yk_max, yy_max) - max(yk_min, yy_min)
                if value_w < 0 or value_h < 0:
                    remain.append(index_c)
                else:
                    value_1 = xk_max - xk_min
                    value_2 = yk_max - yk_min
                    value_3 = value_h * value_w
                    area = (xx_max - xx_min) * (yy_max - yy_min) + value_1 * value_2 - value_3
                    scale = value_3 / area
                    if scale >= c_iou_thresh:
                        extend_TP.append(scale)
                    else:
                        extend_FN.append(scale)
            cube_list = remain
            if len(extend_TP) != 0 and len(extend_FN) != 0:
                list_TP.append(1)
            elif len(extend_TP) != 0 and len(extend_FN) == 0:
                list_TP.append(1)
            elif len(extend_TP) == 0 and len(extend_FN) != 0:
                list_FN.append(1)
            else:
                list_FN.append(1)
        for _ in cube_list:
            list_FP.append(1)
    val = len(list_TP)
    val1 = len(list_FP)
    val2 = len(list_FN)
    print('TP: {0}, FP: {1}, FN: {2}'.format(val, val1, val2))
    print('precision/精确率: {0:.2%}, recall/召回率: {1:.2%}'.format(val / (val + val1), val / (val + val2)))


def read_json_2(r_argv_save_json):
    with open(r_argv_save_json, 'r', encoding='utf-8') as h:
        json_list = json.load(h, encoding='utf-8')
        index = 0
        for i in tqdm(json_list):
            file = i["objects"]
            if len(file) == 0:
                pass
            else:
                index += len(file)
        print('检测错误总数量:{}'.format(index))


if __name__ == '__main__':
    args = parser()
    darknet(args.data_file, args.config_file, args.weights, args.out_json, args.input, args.convert_txt, args.thresh,
            args.raw_lab, args.iou_thresh)
