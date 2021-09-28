def game():
    b = {}
    i = 1
    for x in range(1, 41):
        b[x] = i
        if i == 9:
            i = 0
        i += 1
    return b


all_list = []
"""
约瑟夫生者死者小游戏30 个人在一条船上，超载，需要 15 人下船。
于是人们排成一队，排队的位置即为他们的编号。
报数，从 1 开始，数到 9 的人下船。
如此循环，直到船上仅剩 15 人为止，问都有哪些编号的人下船了呢？
"""


def game_two(h):
    while True:
        if len(h) == 15:  # 船上还剩余人数
            print('下船数量跟号数: ', all_list)
            break
        else:
            list_p = []
            for key, value in h.items():
                if value == 9:
                    list_p.append(key)
                    all_list.append(key)
            unm = 1
            lg = 0
            for key_s, value_s in h.items():
                if key_s == list_p[-1]:
                    lg = len(h) - unm
                unm += 1
            if lg > 0:
                list_1 = list(h.keys())[-lg:] + list(h.keys())[:-lg]
                list_2 = list(h.values())[-lg:] + list(h.values())[:-lg]
                dict_new = dict(zip(list_1, list_2))
            else:
                dict_new = h
            for p in list_p:
                del dict_new[p]
                if len(dict_new) == 15:
                    break
            unm_2 = 1
            for key_ss, value_ss in dict_new.items():
                dict_new[key_ss] = unm_2
                if unm_2 == 9:
                    unm_2 = 0
                unm_2 += 1
            h = dict_new
            # if len(dict_new) == 15:
            #     break
            # else:
            #     game_two(dict_new)
        # print(all_list)


if __name__ == '__main__':
    game()
    game_two(h=game())
