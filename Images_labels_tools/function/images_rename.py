import os
from Images_labels_tools.function import public_function
from Images_labels_tools.config import setting


# 获取字典
def img_rename(path_s, list_num):
    num_s = 0
    dict_list = {}
    # enumerate 函数同时列出索引和对应的元素
    for x, x_1 in enumerate(list_num):
        scr = os.path.join(path_s, x_1)
        # 获取文件创建时间避免图片顺序打乱
        x_y = os.path.getctime(scr)
        # 避免同一文件夹再次命名删除相同名称文件
        dst = os.path.join(path_s, str(num_s) + 'new' + list_num[x])
        os.renames(scr, dst)
        dict_list[str(num_s) + 'new' + list_num[x]] = x_y
        num_s += 1
    return dict_list


# 第二次修改
def renames(file_name_s, images_path, first, number):
    # 以字典值排序，输出为元组式列表[(a,1), (c,2)]
    # x：相当于字典集合中的一个元组,x[1]: 返回x中的第二个元素，即键值对元组中的值
    dict_sorted = sorted(file_name_s.items(), key=lambda k: k[1], reverse=False)
    num = int(first)
    for x in dict_sorted:
        src_1 = os.path.join(images_path, x[0])
        # 第三个参数必须大于第二个images总数张数长度
        poor = int(number) - len(str(num))
        dst_1 = os.path.join(images_path, '0' * poor + str(num) + '.jpg')
        os.rename(src_1, dst_1)
        print('\r修改进度:{0:.2%}'.format((num - int(first) + 1) / len(os.listdir(images_path))), end='')
        num += 1
    print()


def start_images_rename():
    images_path = public_function.Public().img_path
    first = setting.dict_rename['start_number']
    number = setting.dict_rename['images_len']
    list_dir = os.listdir(images_path)
    file_name_s = img_rename(images_path, list_num=list_dir)
    renames(file_name_s, images_path, first, number)
    print()
    print('总共:{0}张图'.format(len(os.listdir(images_path))))
