#!/home/zhoup/anaconda3/envs/python37/bin/python3.7
# -*- coding: utf-8 -*-
# zhoupeng

# os 模块提供了许多与操作系统交互的函数:
# 对于日常文件和目录管理任务， shutil 模块提供了更易于使用的更高级别的接口:
# glob 模块提供了一个在目录中使用通配符搜索创建文件列表的函数:
# 通用实用程序脚本通常需要处理命令行参数。这些参数作为列表存储在 sys 模块的 argv 属性中
# sys 模块还具有 stdin ， stdout 和 stderr 的属性。后者对于发出警告和错误消息非常有用，即使在 stdout 被重定向后也可以看到它们:
# argparse 模块提供了一种更复杂的机制来处理命令行参数。 以下脚本可提取一个或多个文件名，并可选择要显示的行数:
# re 模块为高级字符串处理提供正则表达式工具。对于复杂的匹配和操作，正则表达式提供简洁，优化的解决方案:
# math 模块提供对浮点数学的底层C库函数的访问:
# 有许多模块可用于访问互联网和处理互联网协议。其中两个最简单的 urllib.request 用于从URL检索数据，以及 smtplib 用于发送邮件:
# datetime 模块提供了以简单和复杂的方式操作日期和时间的类。虽然支持日期和时间算法，但实现的重点是有效的成员提取以进行输出格式化和操作。该模块还支持可感知时区的对象。
# 常见的数据存档和压缩格式由模块直接支持，包括：zlib, gzip, bz2, lzma, zipfile 和 tarfile。:
# 与 timeit 的精细粒度级别相反， profile 和 pstats 模块提供了用于在较大的代码块中识别时间关键部分的工具。
# reprlib 模块提供了一个定制化版本的 repr() 函数，用于缩略显示大型或深层嵌套的容器对象:
# textwrap 模块能够格式化文本段落，以适应给定的屏幕宽度:
# locale 模块处理与特定地域文化相关的数据格式。locale 模块的 format 函数包含一个 grouping 属性，可直接将数字格式化为带有组分隔符的样式:
# str.zfill(width) 返回原字符串的副本，在左边填充 ASCII '0' 数码使其长度变为 width。
# 正负值前缀 ('+'/'-') 的处理方式是在正负符号 之后 填充而非在之前。 如果 width 小于等于 len(s) 则返回原字符串的副本。

print("42".zfill(5))
print('44444'.center(21, '*'))
# 返回原序列的副本，移除指定的开头和末尾字节。
print('www.example.com'.strip('w.com'))
# 返回字典 d 中使用的所有键的列表zip([值], [键])
print(list(dict(zip(['one', 'two', 'three'], [1, 2, 3]))))
# 返回由字典值组成的一个新视图
d = {'a': 1}
print(d.values())