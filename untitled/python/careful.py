#!/home/zhoup/anaconda3/envs/python37/bin/python3.7
# -*- coding: utf-8 -*-
# zhoupeng

"""
1.在交互式解释器中，输出的字符串外面会加上引号，特殊字符会使用反斜杠来转义。
如：>>> print('"Isn\'t," they said.')
        "Isn't," they said.
2.如果你不希望前置了'\'的字符转义成特殊字符，可以使用 原始字符串 方式，在引号前添加 r 即可:
"""

# 字符串中的回车换行会自动包含到字符串中，如果不想包含，在行尾添加一个 \ 即可。如下例:
print('''\
333
444
''')
print('1''2''3')

'''
x[:]切片会返回列表的一个新的(浅)拷贝等价于copy
如果在循环内需要修改序列中的值（比如重复某些选中的元素），推荐你先拷贝一份副本。对序列进行循环不代表制作了一个副本进行操作。切片操作使这件事非常简单：
如果写成 for w in words:，这个示例就会创建无限长的列表，一次又一次重复地插入 defenestrate。
'''
x = [1, 2, 3, 4, 5, 6]
for i in x[:]:
    if i > 4:
        x.insert(0, i)
        print(x)


# 如果你不想要在后续调用之间共享默认值，你可以这样写这个函数:
def f(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L


print(f(1))
print(f(2))


# 函数标注
def f(ham: str, eggs: str = 'eggs') -> str:
    print("Annotations:", f.__annotations__)
    print("Arguments:", ham, eggs)
    return ham + ' and ' + eggs


print(f('60'))

# 元组与字符串类似，下标索引从 0 开始，可以进行截取，组合等,元组中的元素值是不允许修改的
# 集合是由不重复元素组成的无序的集。它的基本用法包括成员检测和消除重复元素。集合对象也支持像 联合，交集，差集，对称差分等数学运算。
# 花括号或 set() 函数可以用来创建集合。注意：要创建一个空集合你只能用 set() 而不能用 {}，因为后者是创建一个空字典
'''
与以连续整数为索引的序列不同，字典是以 关键字 为索引的，关键字可以是任意不可变类型，通常是字符串或数字。如果一个元组只包含字符串、数字或元组，
那么这个元组也可以用作关键字。但如果元组直接或间接地包含了可变对象，那么它就不能用作关键字。列表不能用作关键字，
因为列表可以通过索引、切片或 append() 和 extend() 之类的方法来改变。
'''


# dict默认是一key值返回
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k in knights:
    print(k)

# 当你不需要花哨的输出而只是想快速显示某些变量以进行调试时，可以使用 repr() or str() 函数将任何值转化为字符串。

# 还有另外一个方法，str.zfill() ，它会在数字字符串的左边填充零。它能识别正负号:

# 我把任何跟在一个点号之后的名称都称为 属性 --- 例如，在表达式 z.real 中
# 按严格的说法，对模块中名称的引用属于属性引用：在表达式 modname.funcname 中，modname 是一个模块对象而 funcname 是它的一个属性
# 在此情况下在模块的属性和模块中定义的全局名称之间正好存在一个直观的映射：它们共享相同的命名空间！
# global 语句可被用来表明特定变量生存于全局作用域并且应当在其中被重新绑定；nonlocal 语句表明特定变量生存于外层作用域中并且应当在其中被重新绑定


def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)


scope_test()
print("In global scope:", spam)

# 请注意 局部 赋值（这是默认状态）不会改变 scope_test 对 spam 的绑定。 nonlocal 赋值会改变 scope_test 对 spam 的绑定，
# 而 global 赋值会改变模块层级的绑定。
# 您还可以在 global 赋值之前看到之前没有 spam 的绑定。
# 属性引用 使用 Python 中所有属性引用所使用的标准语法: obj.name。 有效的属性名称是类对象被创建时存在于类命名空间中的所有名称
# 一般来说，实例变量用于每个实例的唯一数据，而类变量用于类的所有实例共享的属性和方法:

# glob 模块提供了一个在目录中使用通配符搜索创建文件列表的函数:
import glob
print(glob.glob('*.py'))

# argparse 模块提供了一种更复杂的机制来处理命令行参数。 以下脚本可提取一个或多个文件名，并可选择要显示的行数

# sys 模块还具有 stdin ， stdout 和 stderr 的属性。后者对于发出警告和错误消息非常有用，即使在 stdout 被重定向后也可以看到它们
# sys.stderr.write('Warning, log file not found starting a new one\n')
