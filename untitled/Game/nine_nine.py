i = 1  # 九九乘法表
while i <= 9:
    x = 1
    while x <= i:
        print(str(x) + "*" + str(i) + "=" + str(x * i), end="\t")  # \t表格格式化
        x += 1
    print()
    i += 1
