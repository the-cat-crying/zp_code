def num(n, m):
    a, b = 0, 1
    while m < n:
        if m < 2:
            print(m)
        else:
            a, b = b, a + b
            c = yield b  # 有yield则为一个生成器，m=(i for i in range(0, 9))是一个生成器
            print(c)
        m += 1


t = num(13, 0)
print(next(t))  # 获取生成器下一个元素
print(t.send("good"))  # send方法相当于取下一个元素和为yield赋值并且不能为第一个元素赋值，yield相当于return
print(t.send("tt"))
print(type(t))
