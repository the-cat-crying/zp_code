# -*- coding:utf-8 -*-
# 作者:周鹏
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Images_labels_tools.main import mains


if __name__ == '__main__':
    mains.run()
