# -*- coding:utf-8 -*-
# 作者:周鹏
import socket

# 服务端
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('127.0.0.1', 8080)
server_socket.bind(address)
server_socket.listen(3)
print('waiting.....')
while True:
    client_conn, client_addr = server_socket.accept()
    while True:
        num = bytes()
        data_len = client_conn.recv(30)
        if data_len == b'':
            print('对方已终止链接')
            break
        client_conn.send(bytes('ok', 'utf8'))

        while len(num) != int(str(data_len, 'utf8')):
            data = client_conn.recv(56)
            num += data
        print('>>>', str(num, 'utf8'))
        try:
            data_1 = input('<<<')
        except KeyboardInterrupt:
            break
        else:
            client_conn.send(bytes(data_1, 'utf8'))
