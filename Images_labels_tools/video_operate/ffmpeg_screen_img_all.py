import os
import sys
import time


def print_run_time(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print("this is" + func.__name__ + "all time {0:.6f}".format(end_time - start_time))
    return inner


@print_run_time
def screen(listdir_v, video_p, screens, start_num, length):
    new_img_path = os.path.join(screens, 'new_img')
    os.makedirs(new_img_path)
    count_all, glob = [], 1
    for i in listdir_v:
        abs_path = os.path.join(video_p, i)
        os.system(f"cd {screens} && mkdir {i} && cd {i} && ffmpeg -i {abs_path} -r 1 -qscale 4 -f image2 %06d.jpg")
        new_path_screen = os.path.join(screens, i)
        listdir_img = os.listdir(new_path_screen)
        count_all.append(len(listdir_img))
        if glob == 1:
            x = 0
            for k in listdir_img:
                old = os.path.join(new_path_screen, k)
                numbers = int(start_num) + x
                num_length = '0' * (int(length) - len(str(numbers)))
                path_k = os.path.join(new_img_path, num_length + str(numbers) + '.jpg')
                os.renames(old, path_k)
                x += 1
        else:
            number = sum(count_all[0:glob-1])
            for m in listdir_img:
                path_2 = os.path.join(new_path_screen, m)
                new_number = int(m.split('.')[0]) + number + int(start_num) - 1
                str_number = "".join(["0" * (int(length)-len(str(new_number))), str(new_number), '.jpg'])
                path_new_2 = os.path.join(new_img_path, str_number)
                os.renames(path_2, path_new_2)
        glob += 1


if __name__ == '__main__':
    # 根据配套文件夹使用也可以自行更改路径
    argv_1 = sys.argv[1]  # video_path
    start_nums = input('请输入开始序号，例如1,2,3: ')
    lengths = input('请输入序号长度，例如6,7,8: ')
    screenshot = os.path.join(argv_1, 'screenshot')
    if not os.path.exists(screenshot):
        os.makedirs(screenshot)
    listdir_video = os.listdir(argv_1)
    listdir_video.sort()
    screen(listdir_video, argv_1, screenshot, start_nums, lengths)
