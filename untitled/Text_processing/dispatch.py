from xlrd import xldate_as_tuple
import xlrd
import os
import sys
import datetime
from datetime import datetime as dt
import time
import xlwt
from xlutils.copy import copy


# 运行时间函数
def print_run_time(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        print('\n')
        print('--current function [%s] run time is %.2fs\n' % (func.__name__, time.time() - local_time))
    return wrapper


# 只能读不能写
def read_excel(args, variable, number):
    value_all = []
    excel_path = os.path.join(variable, args[0])
    data = xlrd.open_workbook(excel_path)  # 打开一个excel
    sheet = data.sheet_by_index(number)  # 根据要求获取工作表sheet
    # cel = sheet.row_values(0)  # 获取第一行数据
    for y in range(1, sheet.nrows):  # 行
        rows_list = []
        for x in range(sheet.ncols):  # 列
            ct = sheet.cell(y, x).ctype  # 表格的数据类型
            cel_n = sheet.cell(y, x).value
            if ct == 3:  # python读取excel表格的5种格式,3是时间格式
                date = dt(*xldate_as_tuple(cel_n, 0))  # 转换成python内部的时间格式
                rows_list.append(date.strftime('%Y/%d/%m %H:%M:%S'))  # 时间格式化,统一模式
            else:
                rows_list.append(cel_n)
        value_all.append(rows_list)
    return value_all


def excel_treat(args_t, variable_t):
    index_all = read_excel(args=args_t, variable=variable_t, number=0)
    boarding_port = read_excel(args=args_t, variable=variable_t, number=1)
    aprons_info = read_excel(args=args_t, variable=variable_t, number=2)
    aprons_time = read_excel(args=args_t, variable=variable_t, number=3)
    person = read_excel(args=args_t, variable=variable_t, number=4)
    for i in range(2):
        for add in person:
            add.append(0)
    for ears in index_all:
        if ears[8] == '出港':
            del ears[7]
        else:
            del ears[6]
    flight_data = sorted(index_all, key=lambda s: s[6])
    return flight_data, boarding_port, aprons_info, aprons_time, person


@print_run_time
def dispatch(args_d, var_d, var_s, bus_num, vip_num):
    value_f = 1
    flight_d, waite_p, aprons_in, aprons_t, persons = excel_treat(args_d, var_d)
    bus_car, vip_car = shuttle_bus(bus_num, vip_num)
    save_path = create_2(var_s)
    letter = [chr(i) for i in range(65, 91)]  # 大写字母A~Z
    for i_f in flight_d:
        examples = []
        for math in range(0, 4):
            examples.append([i_f[1], i_f[9], i_f[10], i_f[8], '', '', i_f[11] + i_f[7], math+1, i_f[6], '', '', '', '',
                             '', '', '', '', '', ''])
        if i_f[7] == '出港':
            # 字符串时间转化为可计算时间
            c_time = datetime.datetime.strptime(i_f[6], '%Y/%d/%m %H:%M:%S')
            for i_w in waite_p:
                if i_f[9] == '' and i_f[10] == '':
                    pass
                elif i_f[9] == '' and i_f[10][0] in letter or i_f[10] == '' and i_f[9][0] in letter:
                    if i_f[9] == i_w[0] or i_f[10] == i_w[0]:
                        plain_s = str(int(i_w[4])) + '号坪'
                        bus_car = write_bus(aprons_t, plain_s, bus_car)  # 更新摆渡车开到本次机坪所需时间
                        vip_car = write_bus(aprons_t, plain_s, vip_car)
                        chu_gang(c_time, bus_car, vip_car, plain_s, persons, examples, save_path, i_f[7])
            if i_f[9] == '' and i_f[10] == '':
                pass
            elif i_f[9] == '' and i_f[10][0] in letter or i_f[10] == '' and i_f[9][0] in letter:
                pass
            elif i_f[9] == '' and isinstance(int(i_f[10]), int) or i_f[10] == '' and isinstance(int(i_f[9]), int):
                bus_car = write_bus2(aprons_t, bus_car)
                vip_car = write_bus2(aprons_t, vip_car)
                chu_gang(c_time, bus_car, vip_car, '5号坪', persons, examples, save_path, i_f[7])
        else:
            r_time = datetime.datetime.strptime(i_f[6], '%Y/%d/%m %H:%M:%S')
            for entry in aprons_in:  # 都为5号坪
                if i_f[8] == entry[0] and entry[2] == '远机位' or i_f[8] == entry[0] and entry[2] == '远远机位':
                    bus_car = write_bus3(aprons_t, bus_car)
                    vip_car = write_bus3(aprons_t, vip_car)
                    chu_gang(r_time, bus_car, vip_car, '5号坪', persons, examples, save_path, i_f[7])
        value_f += 1
        print('\r{:.2f}%'.format(value_f / len(flight_d)), end='')


def write_bus(aprons_t, plain_s, bus_all):
    for index, apron in enumerate(aprons_t[0]):
        if plain_s == apron:
            for b_car in aprons_t[1:]:
                for g in bus_all:
                    if b_car[0] == g[1]:
                        g[3] = b_car[index]
    return bus_all


def write_bus2(aprons_t, bus_all):
    for p in aprons_t[1:]:
        for u in bus_all:
            if u[1] == p[0]:
                u[3] = p[3]
    return bus_all


def write_bus3(aprons_t, bus_all):
    for p_k in aprons_t[1:]:
        for u_k in bus_all:
            if u_k[1] == p_k[0]:
                u_k[3] = p_k[3]
    return bus_all


# 选出最优摆渡车
def sort_c(bus, bus_arrive):
    send_list_all = []
    k = 0  # 不符合条件的情况下，等到有空闲的摆渡车跳出循环
    for index, seat in enumerate(bus_arrive):
        seat_list = []
        while True:
            y, waite = 0, []
            for index_w, bus_each in enumerate(bus):
                x = datetime.datetime.strptime(bus_each[2], '%Y/%d/%m %H:%M:%S')
                # 上次结束时间加上本次需要到达机坪时间为需要到达时间
                bus_each[5] = (x + datetime.timedelta(minutes=int(bus_each[3]))).strftime('%Y/%d/%m %H:%M:%S')
                y = datetime.datetime.strptime(seat, '%Y/%d/%m %H:%M:%S')
                if datetime.datetime.strptime(bus_each[5], '%Y/%d/%m %H:%M:%S') <= y:  # 本次摆渡车到达时间大于等于其他车到达时间
                    seat_list.append([bus_each, index_w])
                    bus_arrive[index] = y.strftime('%Y/%d/%m %H:%M:%S')
                else:
                    waite.append(1)
            if len(waite) != len(bus):
                break
            else:
                seat = (y + datetime.timedelta(minutes=1)).strftime('%Y/%d/%m %H:%M:%S')
                k += 1
        send_car = sorted(seat_list, key=lambda s: s[0][5])
        send_list_all.append(send_car[0])
        del bus[send_car[0][1]]
    return bus, send_list_all, k


def judge(time_all, argv_c, index_c1, digit_c1, index_c2, digit_c2, index_c3, digit_c3, index_c4, digit_c4, index_r1,
          digit_r1, index_r2, digit_r2, index_r3, digit_r3, index_r4, digit_r4):
    if argv_c == '出港':
        bus_car_1, bus_car_2 = time_k(time_all, index_c1, digit_c1), time_k(time_all, index_c2, digit_c2)
        bus_car_3, vip_car_1 = time_k(time_all, index_c3, digit_c3), time_k(time_all, index_c4, digit_c4)
    else:
        bus_car_1, bus_car_2 = time_k(time_all, index_r1, digit_r1), time_k(time_all, index_r2, digit_r2)
        bus_car_3, vip_car_1 = time_k(time_all, index_r3, digit_r3), time_k(time_all, index_r4, digit_r4)
    return bus_car_1, bus_car_2, bus_car_3, vip_car_1


def time_k(a_time, value, num):
    return (a_time + datetime.timedelta(minutes=(-float(value) + num))).strftime('%Y/%d/%m %H:%M:%S')


def chu_gang(send_c, bus_car, vip_car, plain_c, persons, examples, save_path, argv_c):
    bus_reach = []
    # 摆度车原有到达时间
    bus_d_1, bus_d_2, bus_d_3, vip_d_1 = judge(send_c, argv_c, 0, -35, 0, -25, 0, -19, 0, -35, 0, -5, 0, 0, 0, 5, 0, -5)
    bus_reach.extend([bus_d_1, bus_d_2, bus_d_3, vip_d_1])  # 在末尾添加多个元素

    bus_car, send_bus, add_tb = sort_c(bus_car, bus_reach[0:3])
    vip_car, send_vip, add_tv = sort_c(vip_car, bus_reach[3:4])
    # 摆渡车延迟后新的计算时间
    new_time = (send_c + datetime.timedelta(minutes=int(add_tb + add_tv))).strftime('%Y/%d/%m %H:%M:%S')
    new_times = datetime.datetime.strptime(new_time, '%Y/%d/%m %H:%M:%S')

    # 摆渡车延迟后结束工作时间
    f1, f2, f3, f4 = send_bus[0][0][3], send_bus[1][0][3], send_bus[2][0][3], send_vip[0][0][3]
    f_c_end, s_c_end, t_c_end, vip_c_end = judge(new_times, argv_c, -(2*f1+1), -25, -(2*f2+1), -19, -(2*f3+1), -5,
                                                 -(2*f4+1), -15, -(1.5*f1+1), 13, -(1.5*f1+1), 15, -(1.5*f1+1), 17,
                                                 -(1.5*f1+1), 13)
    # 摆渡车延迟后新启动时间
    first_car, second_car, third_car, vip_v_car = judge(new_times, argv_c, f1, -35, f2, -25, f3, -19, f4, -35, f1,
                                                        -5, f2, 0, f3, 5, f4, -5)
    # 人员分配和工作时间和更新开始时间和结束时间
    add_a, first_car, f_c_end, second_car, s_c_end, third_car, t_c_end, vip_v_car, vip_c_end = \
        portion(first_car, f_c_end, second_car, s_c_end, third_car, t_c_end, vip_v_car, vip_c_end, persons, examples)
    # 人员延迟后新的计算时间
    new_tp = (new_times + datetime.timedelta(minutes=int(sum(add_a)))).strftime('%Y/%d/%m %H:%M:%S')
    new_tps = datetime.datetime.strptime(new_tp, '%Y/%d/%m %H:%M:%S')
    # 摆度车新到达时间
    bus_n_1, bus_n_2, bus_n_3, vip_n_1 = judge(new_tps, argv_c, 0, -35, 0, -25, 0, -19, 0, -35, 0, -5, 0, 0, 0, 5,
                                               0, -5)
    # 摆度车新出发时间
    bus_cf_1, bus_cf_2, bus_cf_3, vip_cf_1 = judge(new_tps, argv_c, 0, -25, 0, -19, 0, -5, 0, -15, 0, 13, 0, 15,
                                                   0, 17, 0, 13)
    # 写入excel数据
    examples[0][4], examples[1][4] = send_bus[0][0][0], send_bus[1][0][0]
    examples[2][4], examples[3][4] = send_bus[2][0][0], send_vip[0][0][0]

    examples[0][5], examples[1][5] = send_bus[0][0][4], send_bus[1][0][4]
    examples[2][5], examples[3][5] = send_bus[2][0][4], send_vip[0][0][4]

    examples[0][9], examples[1][9], examples[2][9], examples[3][9] = first_car, second_car, third_car, vip_v_car
    examples[0][10], examples[1][10], examples[2][10], examples[3][10] = bus_n_1, bus_n_2, bus_n_3, vip_n_1
    examples[0][11], examples[1][11], examples[2][11], examples[3][11] = bus_cf_1, bus_cf_2, bus_cf_3, vip_cf_1
    examples[0][12], examples[1][12], examples[2][12], examples[3][12] = f_c_end, s_c_end, t_c_end, vip_c_end

    examples[0][13] = str(datetime.datetime.strptime(f_c_end, '%Y/%d/%m %H:%M:%S') -
                          datetime.datetime.strptime(first_car, '%Y/%d/%m %H:%M:%S'))
    examples[1][13] = str(datetime.datetime.strptime(s_c_end, '%Y/%d/%m %H:%M:%S') -
                          datetime.datetime.strptime(second_car, '%Y/%d/%m %H:%M:%S'))
    examples[2][13] = str(datetime.datetime.strptime(t_c_end, '%Y/%d/%m %H:%M:%S') -
                          datetime.datetime.strptime(third_car, '%Y/%d/%m %H:%M:%S'))
    examples[3][13] = str(datetime.datetime.strptime(vip_c_end, '%Y/%d/%m %H:%M:%S') -
                          datetime.datetime.strptime(vip_v_car, '%Y/%d/%m %H:%M:%S'))
    examples[0][15], examples[1][15] = send_bus[0][0][1], send_bus[1][0][1]
    examples[2][15], examples[3][15] = send_bus[2][0][1], send_vip[0][0][1]
    # 修改派工成功摆度车的位置和时间
    send_bus[0][0][1], send_bus[0][0][2] = plain_c, f_c_end
    send_bus[1][0][1], send_bus[1][0][2] = plain_c, s_c_end
    send_bus[2][0][1], send_bus[2][0][2] = plain_c, t_c_end
    send_vip[0][0][1], send_vip[0][0][2] = plain_c, vip_c_end
    for h in send_bus:
        bus_car.append(h[0])
    for v in send_vip:
        vip_car.append(v[0])
    examples[0][16], examples[1][16], examples[2][16], examples[3][16] = plain_c, plain_c, plain_c, plain_c

    write(save_path, examples)


def portion(first_car, f_c_end, second_car, s_c_end, third_car, t_c_end, vip_v_car, vip_c_end, persons, examples):
    car_time_list = [[first_car, f_c_end, persons], [second_car, s_c_end, persons], [third_car, t_c_end, persons],
                     [vip_v_car, vip_c_end, persons]]
    person_list, add_p = [], []
    for index, value in enumerate(car_time_list):
        send_person, add, st, end = drive(value[0], value[1], value[2])
        if len(send_person) == 0:
            continue
        else:
            person_list.append(send_person)
            add_p.append(add)
            examples[index][14] = send_person[0][0]
            examples[index][17] = send_person[0][3]
            examples[index][18] = send_person[0][2]
        if index == 0:
            first_car, f_c_end = st, end
        elif index == 1:
            second_car, s_c_end = st, end
        elif index == 2:
            third_car, t_c_end = st, end
        else:
            vip_v_car, vip_c_end = st, end
    for up in person_list:
        persons[up[1]] = up[0]
    return add_p, first_car, f_c_end, second_car, s_c_end, third_car, t_c_end, vip_v_car, vip_c_end


def drive(start_time, car_end_time, persons):
    if '2019/14/01 00:00:00' <= start_time <= '2019/14/01 08:00:00':
        return work_time(car_end_time, start_time, persons[0:36], 0, persons)
    elif '2019/14/01 08:00:00' < start_time <= '2019/14/01 16:00:00':
        return work_time(car_end_time, start_time, persons[36:78], 36, persons)
    elif '2019/14/01 16:00:00' < start_time < '2019/14/01 24:00:00':
        return work_time(car_end_time, start_time, persons[78:108], 78, persons)
    else:
        return [], [], [], []


# 选出时间最短符合条件的相关人员
def work_time(end_time_t, start_time_t, person_t, math, persons):
    number, index, send_p = 0, 0, []
    while True:  # 不符合条件的情况下，等到有空闲的人员跳出循环
        person_t = sorted(person_t, key=lambda s: s[3])
        for index_w, each in enumerate(person_t):
            if each[0] == 0:
                continue
            else:
                if str(each[4]) <= start_time_t:
                    if number == 1:
                        break
                    else:
                        end_time_t = (datetime.datetime.strptime(end_time_t, '%Y/%d/%m %H:%M:%S') +
                                      datetime.timedelta(minutes=index)).strftime('%Y/%d/%m %H:%M:%S')
                        drive_t = datetime.datetime.strptime(end_time_t, '%Y/%d/%m %H:%M:%S') - \
                            datetime.datetime.strptime(start_time_t, '%Y/%d/%m %H:%M:%S')
                        each[4] = end_time_t
                        each[3] = drive_t.total_seconds()  # 转换为秒
                        send_p.append(each)
                        send_p.append(index_w+math)
                        persons[index_w+math] = [0, 0, 0, 0]
                        number += 1
        if number == 1:
            break
        else:
            start_time_t = (datetime.datetime.strptime(start_time_t, '%Y/%d/%m %H:%M:%S') +
                            datetime.timedelta(minutes=1)).strftime('%Y/%d/%m %H:%M:%S')
            index += 1
    return send_p, index, start_time_t, end_time_t


def create_2(var_2):
    s_tus = [['航班号', '任务执行登机口1', '任务执行登机口2', '任务执行机位', '派工车型', '车辆编号', '任务类型', '发车车次', '到港/出港时间',
              '开车时间', '到位时间', '发车时间', '结束时间', '任务时长', '人员编号', '起始坪', '结束坪', '工作时间', '工作时间段']]
    books = xlwt.Workbook()  # 新建一个excel
    sheet = books.add_sheet('摆渡车任务示例')  # 添加一个sheet页
    save_path = os.path.join(var_2, 'stu_2.xlsx')
    row = 0  # 控制行
    for stu in s_tus:
        col = 0  # 控制列
        for s in stu:  # 再循环里面list的值，每一列
            sheet.write(row, col, s)
            col += 1
        row += 1
    books.save(save_path)
    return save_path


def write(path_excel, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path_excel)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path_excel)  # 保存工作簿


def shuttle_bus(bus, vip):
    bus_list, vip_list = [], []
    for b in range(1, bus + 1):
        bus_list.append(['COBUS-' + str(b), '3号坪', '2019/13/01 23:51:00', 0, 'COBUS3000', 0])
    for c in range(1, vip + 1):
        vip_list.append(['北方-' + str(c), '3号坪', '2019/13/01 23:51:00', 0, '北方', 0])
    return bus_list, vip_list


def main():
    if len(sys.argv) != 3:
        print('请依次输入基础数据类型表,保存输出位置')
    else:
        argv_1 = sys.argv[1]
        argv_2 = sys.argv[2]
        data_list = os.listdir(argv_1)
        return data_list, argv_1, argv_2


def start():
    data, argv, argv_s = main()
    dispatch(args_d=data, var_d=argv, var_s=argv_s, bus_num=26, vip_num=10)


if __name__ == '__main__':
    # 飞机摆渡车派工以及人工分配
    start()
