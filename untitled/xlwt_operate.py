# from ctypes import *
import os
import xlwt
from tqdm import tqdm


def write(info_list_):
    # base_dir = os.getcwd() # 方法一
    # print(base_dir)
    # NameError: name '__file__' is not defined
    # 当python在终端或者说在交互式情况下运行时，是无法识别__file__的。 此时要获取当前脚本运行的目录可以使用 os.path.abspath('')
    pwd = os.path.dirname(os.path.abspath(__file__))
    work_book = xlwt.Workbook(encoding='utf-8')
    sheet = work_book.add_sheet('sheet表名', cell_overwrite_ok=True)
    myStyle = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')  # 数据格式
    # 设置边框
    borders = xlwt.Borders()
    # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
    # 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    borders.left_colour = 0
    borders.right_colour = 0
    borders.top_colour = 0
    borders.bottom_colour = 0

    style3 = xlwt.XFStyle()
    style3.borders = borders

    index = len(info_list_)  # 获取需要写入数据的行数
    # 写入图片数据
    # number = 0
    # for i in range(0, index):
    #     sheet.write(number, 0, u"".join(["第", str(i + 1), "张"]), myStyle)
    #     sheet.write(number, 1, ":".join(["fps", str(info_list_[i][0])]))
    #     number += 1
    #     sheet.write(number, 1, "Objects:", style3)
    #     sheet.write(number, 2, "Confidence:", style3)
    #     list_len = len(info_list_[i])
    #     if list_len == 1:
    #         pass
    #     else:
    #         for j in range(1, list_len):
    #             sheet.write(number + j, 1, info_list_[i][j][0], style3)  # 追加写入数据，注意是从i+rows_old行开始写入
    #             sheet.write(number + j, 2, info_list_[i][j][1], style3)
    #     number += list_len
    for i in tqdm(range(0, index)):
        if info_list_[i][2] == '':
            sheet.write(i, 1, info_list_[i][2], style3)
        else:
            sheet.write(i, 1, info_list_[i][2], style3)
    work_book.save(pwd + '/Excel表.xls')  # 保存Excel表,注意表名后面要加.xls后缀
