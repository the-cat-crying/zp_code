a = [[[1, 2, 3], [4, 5, 6]], [7, 8, 9, [10, 11, [12, 13]]], (14, 15), {4: 5, 6: 7}, 'good']  # 任意列表嵌套列表


def x(k):
    for i in k:
        if isinstance(i, (int, float, str, dict, tuple)):  # 可以添加任意数据类型
            print(i, end=' ')
        else:
            x(i)


x(a)
