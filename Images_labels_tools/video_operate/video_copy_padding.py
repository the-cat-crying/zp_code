import os
import tqdm
import numpy as np
from Images_labels_tools.function import public_function
from Images_labels_tools.config import setting
import time
import cv2


def images_operate(i_img_list, i_save_w, i_save_h, i_cap_saved_video, i_args):
    number = 0
    for index in tqdm.tqdm(i_img_list):
        old_height, old_width, old_channel = index.shape
        scale_h = i_save_h // old_height
        scale_w = i_save_w // old_width
        differ_h = i_save_h - old_height * scale_h
        differ_w = i_save_w - old_width * scale_w
        # np.uint8不能少
        np_zero = np.zeros((i_save_h, i_save_w, old_channel), np.uint8)
        # 这种拼接方式固定张数
        # img = cv2.hconcat([index, index, index])  # 水平拼接
        # img = cv2.vconcat([img, img, img])  # 垂直拼接

        for i in range(0, scale_h):
            min_h = old_height * i
            max_h = old_height * (i + 1)
            for j in range(0, scale_w):
                min_w = old_width * j
                max_w = old_width * (j + 1)
                np_zero[min_h:max_h, min_w:max_w, :] = index[:, :, :]
            if differ_w > 0:
                np_zero[min_h:max_h, i_save_w - differ_w:i_save_w, :] = index[:, 0:differ_w, :]
        if differ_h > 0:
            for k in range(0, scale_w):
                min_w2 = old_width * k
                max_w2 = old_width * (k + 1)
                np_zero[i_save_h - differ_h:i_save_h, min_w2:max_w2, :] = index[0:differ_h, :, :]
        if differ_h > 0 and differ_w > 0:
            np_zero[i_save_h - differ_h:i_save_h, i_save_w - differ_w:i_save_w, :] = index[0:differ_h, 0:differ_w, :]
        if i_args.save == 'vid':
            i_cap_saved_video.write(np_zero)
        elif i_args.save == 'img':
            save_img_path = os.path.join(i_cap_saved_video, str(number) + '.jpg')
            cv2.imwrite(save_img_path, np_zero)
            number += 1
    if i_args.save == 'vid':
        i_cap_saved_video.release()


def start():
    cap_saved_video = 0
    argv_1 = public_function.Public().img_path
    argv_2 = setting.video_copy_padding['out_width']
    argv_3 = setting.video_copy_padding['out_height']
    argv_4 = public_function.Public().picture_operate()
    args = setting.args
    times = time.localtime()
    time_str = time.strftime("%Y_%m_%d_%H_%M_%S", times)
    if args.demo == 'video':
        path = public_function.mkdir(argv_1, 'new_video')
        save_video_path = os.path.join(path, time_str + '_camera.mp4')
        if os.path.isdir(argv_1):
            video_list = os.listdir(argv_1)
            video_list.sort()
            for index in video_list:
                video_path = os.path.join(argv_1, index)
                cap_saved_video = public_function.set_saved_video(video_path, save_video_path, (argv_2, argv_3))
                images_list = public_function.read_video(video_path)
                images_operate(images_list, argv_2, argv_3, cap_saved_video, args)
        if os.path.isfile(argv_1):
            images_list = public_function.read_video(argv_1)
            cap_saved_video = public_function.set_saved_video(argv_1, save_video_path, (argv_2, argv_3))
            images_operate(images_list, argv_2, argv_3, cap_saved_video, args)
    elif args.demo == 'images':
        if args.save == 'vid':
            path = public_function.mkdir(argv_1, 'new_video')
            save_video_path = os.path.join(path, time_str + '_camera.mp4')
            cap_saved_video = public_function.set_saved_video(argv_1, save_video_path, (argv_2, argv_3))
        elif args.save == 'img':
            cap_saved_video = public_function.mkdir(argv_1, 'cut_images')
        argv_list = []
        for o in argv_4:
            argv_list.append(cv2.imread(o))
        images_operate(argv_list, argv_2, argv_3, cap_saved_video, args)
