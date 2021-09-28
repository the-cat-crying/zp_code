import os
import sys
import shutil


# 标签类别合并
def write(labels_1, labels_2):
    for i in labels_1:
        if i in labels_2:
            path_1 = os.path.join(argv_1, i)
            with open(path_1, 'r') as file:
                file_path = os.path.join(argv_2, i)
                with open(file_path, "a") as file_w:
                    file_w.writelines(file)


# 把在A文件夹移动到B文件夹中(在A中不在B中的文件)
def write_not(labels_3, labels_4):
    h = set(labels_3) - set(labels_4)
    list_1 = list(h)
    for b in list_1:
        scr = os.path.join(argv_1, b)
        dst = os.path.join(argv_2, b)
        shutil.move(scr, dst)


if __name__ == '__main__':
    # 适用于每类别单独标注完最后再把所有类别合并起来
    argv = sys.argv[:]  # all labels path
    for k in range(1, len(argv)-1):
        argv_1 = sys.argv[k]
        argv_2 = sys.argv[k + 1]
        listdir_1 = os.listdir(argv_1)
        listdir_1.sort()
        listdir_2 = os.listdir(argv_2)
        listdir_2.sort()
        write(labels_1=listdir_1, labels_2=listdir_2)
        write_not(labels_3=listdir_1, labels_4=listdir_2)
    print('合并结果在:', sys.argv[len(argv)-1])
