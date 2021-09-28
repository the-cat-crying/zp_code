# -*- coding:utf-8 -*-
# 作者:周鹏
# 计算器
import re
import sys


def calculate(primeval_num):
    while re.search(r'\(', primeval_num):
        for i in re.finditer(r'\([^()]+\)', primeval_num):
            ret = i.group()
            good = ret
            ret = add_sub_mul_div(ret)
            primeval_num = primeval_num.replace(good, ret, 1)
        primeval_num = symbol(primeval_num)
        primeval_num = brackets(primeval_num)
        primeval_num = symbol(primeval_num)
    else:
        while re.search('[/*+-]', primeval_num):
            primeval_num = symbol(primeval_num)
            primeval_num = add_sub_mul_div(primeval_num)
            primeval_num = symbol(primeval_num)
    print(primeval_num)


def add_sub_mul_div(fist_number_str):
    while re.findall('[/*]', fist_number_str):
        mounts = re.search(r'(\d*\.?\d+)[*/]([-]?\d*\.?\d+)', fist_number_str)
        fist_number_str = multiply_and_divide(fist_number_str, mounts)

    while re.findall(r'[-]?(\d*\.?\d+)[+-](\d*\.?\d+)', fist_number_str):
        ad = re.search(r'[-]?(\d*\.?\d+)[+-](\d*\.?\d+)', fist_number_str)
        fist_number_str = addition_and_subtraction(fist_number_str, ad)
    return fist_number_str


def multiply_and_divide(fist_str, number_str):
    mount = number_str.group(1)
    mount_2 = number_str.group(2)
    if re.search(r'\*', number_str.group()):
        ret_m = str(float(mount) * float(mount_2))
        fist_str = fist_str.replace(number_str.group(), ret_m, 1)
    else:
        ret_m = str(float(mount) / float(mount_2))
        fist_str = fist_str.replace(number_str.group(), ret_m, 1)
    return fist_str


def addition_and_subtraction(fist_str, number_str):
    if len(re.findall('[+-]', number_str.group())) == 2:
        number_1 = ''.join(['-', number_str.group(1)])
        number_2 = number_str.group(2)
    else:
        number_1 = number_str.group(1)
        number_2 = number_str.group(2)
    if re.search(r'\+', number_str.group()):
        ret_a = str(float(number_1) + float(number_2))
        fist_str = fist_str.replace(number_str.group(), ret_a, 1)
    else:
        ret_a = str(float(number_1) - float(number_2))
        fist_str = fist_str.replace(number_str.group(), ret_a, 1)
    return fist_str


def brackets(str_num):  # 去括号
    for b in re.finditer(r'\([^()]+\)', str_num):
        bracket = b.group()
        k = bracket
        str_num = str_num.replace(k, bracket[1:-1], 1)
        # list_re = re.findall(r'[^()\d.]', bracket)
        # if len(list_re) == 1 or len(list_re) == 0:
        #     number = re.search(r'[/*+-]?\d*\.\d*', bracket).group()
        #     str_num = str_num.replace(k, number, 1)
    return str_num


def symbol(primeval):  # 去重复括号
    if re.search('[a-zA-Z]', primeval):
        print('请输入正确的数字！', primeval)
        sys.exit()
    primeval_r = primeval.replace(' ', '')
    for p in re.finditer(r'[*+-][+-]', primeval_r):
        if p.group() == '+-' or p.group() == '-+':
            primeval_r = primeval_r.replace(p.group(), '-', 1)
        elif p.group() == '++' or p.group() == '--':
            primeval_r = primeval_r.replace(p.group(), '+', 1)
        elif p.group() == '*+' or p.group() == '+*':
            primeval_r = primeval_r.replace(p.group(), '*', 1)
        elif p.group() == '/+' or p.group() == '+/':
            primeval_r = primeval_r.replace(p.group(), '/', 1)
        elif p.group() == '-*' or p.group() == '-/':
            print('请检查输入是否有"-*","-/"错误')
        else:
            pass
    return primeval_r


if __name__ == '__main__':
    # s = '1-2*((60-30+(-40/5)*(9-2*8/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
    number_all = input('请输入需要计算的式子:')
    # print(eval(s))
    number_a = symbol(number_all)
    calculate(number_a)
