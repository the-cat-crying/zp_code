menu = {
    "北京": {"东城区": {"老男孩": {}}, "西城区": {"嘻嘻哈": {}}, "朝阳区": {"嘟嘟嘟": {}}},
    "四川": {"成都市": {"成华区": {}}, "资阳市": {"雁江区": {}}, "南充市": {"高坪区": {}}},
    "云南": {"昆明市": {"盘龙区": {}}, "曲靖市": {"马龙区": {}}, "邵通市": {"大关县": {}}}
}


# 菜单搜索和返回
father = []
while True:
    for key in menu:
        print(key)
    in_put = input("<<<")
    if in_put in menu:  # 默认以dict.key执行
        father.append(menu)  # 将上一层所有的dict.key保存在list中
        menu = menu[in_put]
    elif not father:
        pass
    elif in_put == "d":
        menu = father.pop()  # 删除list最后一个元素
    else:
        print("用餐愉快！")
