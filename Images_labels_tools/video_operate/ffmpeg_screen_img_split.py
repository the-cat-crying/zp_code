import os
import sys
import time
import shutil


def print_run_time(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print("this is function all time {0:.6f}".format(end_time - start_time))
    return inner


@print_run_time
def screen(listdir_v, video_p, screens):
    os.makedirs(os.path.join(screens, 'new_img'))
    count_all, glob = [], 1
    for i in listdir_v:
        abs_path = os.path.join(video_p, i)
        os.system(f"cd {screens} && mkdir {i} && cd {i} && ffmpeg -i {abs_path} -r 1 -qscale 4 -f image2 %06d.jpg")
        new_path_screen = os.path.join(screens, i)
        listdir_img = os.listdir(new_path_screen)
        count_all.append(len(listdir_img))
        if glob == 1:
            shutil.move(new_path_screen, os.path.join(screens, 'new_img'))
        else:
            create_mkdir = os.path.join(screens, 'new_img', i)
            os.makedirs(create_mkdir)
            number = sum(count_all[0:glob-1])
            for m in listdir_img:
                path_2 = os.path.join(new_path_screen, m)
                new_number = int(m.split(".")[0]) + number
                str_number = "".join(["0"*(6-len(str(new_number))), str(new_number), '.jpg'])
                path_new_2 = os.path.join(create_mkdir, str_number)
                os.renames(path_2, path_new_2)
        glob += 1


if __name__ == '__main__':
    # 根据配套文件夹使用也可以自行更改路径
    argv_1 = sys.argv[1]  # video_path
    screenshot = os.path.join(argv_1, 'screenshot')
    if not os.path.exists(screenshot):
        os.makedirs(screenshot)
    listdir_video = os.listdir(argv_1)
    listdir_video.sort()
    screen(listdir_video, argv_1, screenshot)
