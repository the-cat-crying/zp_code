# -*- coding:utf-8 -*-
# 作者:周鹏
import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            while True:
                self.data = self.request.recv(1024)
                print("{} send:".format(self.client_address), self.data)
                if not self.data:
                    print("connection lost")
                    break
                self.request.sendall(self.data.upper())
        except Exception as e:
            print(self.client_address, "连接断开")
        finally:
            self.request.close()

    def setup(self):
        print("before handle,连接建立：", self.client_address)

    def finish(self):
        print("finish run  after handle")


HOST, PORT = "localhost", 9999

server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)  # 多线程版
server.serve_forever()
