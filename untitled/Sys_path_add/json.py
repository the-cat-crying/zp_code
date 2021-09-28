# -*- coding:utf-8 -*-
# 作者:周鹏
import json
f = {'fly': {'good': 'haply'}}
with open('../Text_processing/good.json', 'w') as g:
    json.dump(f, g)  # json.dump编码文件内容
with open('../Text_processing/good.json', 'r') as h:
    print(json.load(h, encoding='utf-8'))  # json.load对文件内容进行解码

dp = json.dumps([1, 2])  # json.dumps和json.loads分别编码成字符串，解码字符串
print(type(dp), dp)
ld = json.loads('{"name": "boy"}')
print(type(ld), ld)
