import time


# 装饰器
def run_time(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print('{0} operation hours {1:.3f}'.format(func.__name__, (end_time - start_time)))
    return inner


@run_time  # 等同于num = run_time(num)的调用
def num():
    n = 0
    for i in range(1, 30):
        n += i
    print(n)


if __name__ == '__main__':
    num()
