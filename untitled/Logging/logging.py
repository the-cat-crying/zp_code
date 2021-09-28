# -*- coding:utf-8 -*-
# 作者:周鹏
import logging  # 引入logging模块
import os.path
import time

# 第一步，创建一个logger文本输出对象
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关,文件或者控制台输出内容都不小于此等级
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/Logging/'
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w')  # 输出到file文件中
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关，此时DEBUG日志不会输出到文件内容中
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)


# 只要在输入到日志中的第二步和第三步插入一个handler输出到控制台：
ch = logging.StreamHandler()  # 创建一个handler，用于输出到控制台
ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关
ch.setFormatter(formatter)  # 添加日子格式化输出
logger.addHandler(ch)  # 将输出控制台对象添加到handler里面
# 日志
logger.debug('this is a logger debug message')
logger.info('this is a logger info message')
logger.warning('this is a logger warning message')
logger.error('this is a logger error message')
logger.critical('this is a logger critical message')
