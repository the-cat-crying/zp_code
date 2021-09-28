# -*- coding:utf-8 -*-
# 作者:周鹏
import socket

# 客户端，聊天工具
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('127.0.0.1', 8080)
client_socket.connect(address)
while True:
    try:
        data = input('<<<')
    except KeyboardInterrupt:
        break
    else:
        if data == 'exit':
            break
        else:
            data_utf = bytes(data, 'utf8')
            data_len = len(data_utf)
            client_socket.send(bytes(str(data_len), 'utf8'))
            client_socket.recv(10)

            client_socket.send(data_utf)
            data_1 = client_socket.recv(1024)
            print('>>>', str(data_1, 'utf8'))
