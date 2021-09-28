# -*- coding:utf-8 -*-
# 作者:周鹏

"""
我们在使用class创建类的时候, 只会创建一个类对象, 但是, 当我们实例化这个类对象的时候, 一个类对象, 可以实例化出很多不同的对象,
而我们每次实例化出来一个对象, 就会在内存中重新分配一块空间, 而今天介绍的单例模式,
就是为了解决上述问题, 使得由一个类对象所实例化出来的全部对象都指向同一块内存空间.
"""


# 但例模式，创建一次对象，后面创建的对象都指向一个地址, 创建的两种方式
class Foo(object):
    __v = None

    def __init__(self):
        print(123)

    @classmethod
    def func(cls):
        if cls.__v:
            return cls.__v
        else:
            cls.__v = Foo()
            return cls.__v


# while True:
f1 = Foo.func()
f2 = Foo.func()
print(f1)
print(f2)


'''
要想弄明白为什么每个对象被实例化出来之后, 都会重新被分配出一块新的内存地址, 就要清楚一个python中的内置函数__new__(), 它跟__init__()一样, 
都是对象在被创建出来的时候, 就自动执行的一个函数, init()函数, 是为了给函数初始化属性值的, 而__new__()这个函数, 就是为了给对象在被实例化的时候, 
分配一块内存地址, 因此, 我们可以重写__new__()这个方法, 让他在第一次实例化一个对象之后, 分配一块地址, 在此后的所有实例化的其他对象时, 
都不再分配新的地址, 而继续使用第一个对象所被分配的地址, 因此, 我们可以在类对象里, 定义一个类属性, 初始值设为None, 
如果这个值是None就调用父类的__new__()方法, 为其分配地址, 并返回这个地址(__new__方法一定要返回一个地址)
'''


class Food(object):
    __v = None
    flag = True

    def __new__(cls, *args, **kwargs):
        if cls.__v is None:
            cls.__v = super().__new__(cls)
        return cls.__v

    def __init__(self):  # 这种操作为了使__init__只创建一次
        if not Food.flag:
            return
        Foo.flag = False
        print(123)


f3 = Food()
print(f3)
f4 = Food()
print(f4)
