import threading
import time

num = 100
lock = threading.Lock()  # 线程锁，目的是让一个线程运行完在切换到另一个线程，防止随意切换线程，打印错乱


def run(name):
    global num
    lock.acquire()
    if num > 0:
        num -= 1
        print(name, 'a窗口卖出一张票，还剩下: {}'.format(num))
        time.sleep(2)
        lock.release()


if __name__ == '__main__':
    while True:
        if num > 0:
            p1 = threading.Thread(target=run, args=('A窗口',))
            p2 = threading.Thread(target=run, args=('B窗口',))
            p1.start()  # 线程开始
            p2.start()
            p1.join()  # 目的让子线程执行完成在执行主线程
            p2.join()
        else:
            break
    print('票以及卖完')
