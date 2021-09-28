# -*- coding:utf-8 -*-
# 作者:周鹏
import os
import sys


def sys_path_add():  # 这样做的目的就是任何地方都可以运行这个包里面的.py文件
    # print(__file__)  # 打印出当前文件相对路径
    # print(os.path.abspath(__file__))  # 打印出此文件的绝对路径
    # print(os.path.dirname(os.path.abspath(__file__)))  # 查找上一层路径
    # print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # print(sys.path)
    # 把路径添加到python查找系统路径里面，就可以在任何地方找到包路径，使得调用其他包内的.py文件能运行
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(sys.path)


if __name__ == '__main__':
    sys_path_add()
