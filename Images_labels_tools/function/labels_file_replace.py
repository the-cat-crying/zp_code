from Images_labels_tools.function import public_function
from Images_labels_tools.function import labels_operate
from Images_labels_tools.config import setting


def txt_operate(t_argv_1, t_argv_2, t_argv_3, t_argv_4):
    unm = int(input("请输入(1 追加, 2 替换, 3 类别替换): "))
    set_ = labels_operate.txt_set(t_argv_1)
    set_sort = sorted(set_)
    for k in t_argv_1:
        p_list = []
        if unm == 1:
            with open(k, "a") as file_1:
                file_1.write(t_argv_2)
        elif unm == 2:
            l_ = []
            with open(k, "r") as file_2:
                while True:
                    x_1 = file_2.readline()
                    if x_1 == '':
                        break
                    else:
                        x_1 = x_1.replace(t_argv_3, t_argv_4, 1)
                        l_.append(x_1)
            with open(k, "w") as file_write:
                file_write.writelines(l_)
        elif unm == 3:
            with open(k, "r") as file_3:
                u = file_3.readlines()
                for p in u:
                    p_split = p.strip('\n').split(' ')
                    for i in range(0, len(set_sort)):
                        if p_split[0] == set_sort[i]:
                            p_split[0] = str(i)
                            str_ = ' '.join(p_split) + '\n'
                            p_list.append(str_)
            public_function.write_txt(k, p_list)


# 在txt文本中增加或者替换或者类别替换
def start():
    argv_1 = public_function.Public().file_operate()
    argv_2 = setting.labels_replace['lab_add']
    argv_3 = setting.labels_replace['lab_rep_old']
    argv_4 = setting.labels_replace['lab_rep_new']
    txt_operate(argv_1, argv_2, argv_3, argv_4)
