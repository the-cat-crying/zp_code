import requests
import os
import re
import sys
import time
import threading
from urllib import parse
from datetime import datetime as dt
from multiprocessing.dummy import Pool
from multiprocessing import Queue


class Bai_duImgDownloader(object):
    """百度图片下载工具，目前只支持单个关键词"""

    # 解码网址用的映射表
    str_table = {
        '_z2C$q': ':',
        '_z&e3B': '.',
        'AzdH3F': '/'
    }

    char_table = {
        'w': 'a',
        'k': 'b',
        'v': 'c',
        '1': 'd',
        'j': 'e',
        'u': 'f',
        '2': 'g',
        'i': 'h',
        't': 'i',
        '3': 'j',
        'h': 'k',
        's': 'l',
        '4': 'm',
        'g': 'n',
        '5': 'o',
        'r': 'p',
        'q': 'q',
        '6': 'r',
        'f': 's',
        'p': 't',
        '7': 'u',
        'e': 'v',
        'o': 'w',
        '8': '1',
        'd': '2',
        'n': '3',
        '9': '4',
        'c': '5',
        'm': '6',
        '0': '7',
        'b': '8',
        'l': '9',
        'a': '0'
    }

    re_objURL = re.compile(r'"objURL":"(.*?)".*?"type":"(.*?)"')
    re_downNum = re.compile(r"已下载\s(\d+)\s张图片")
    headers = {
        'Referer': 'https://image.baidu.com/search/index',
        "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
        "Accept-Encoding": "gzip, deflate, br",
    }

    def __init__(self, Word, dir_path=None):
        if " " in Word:
            raise AttributeError("本脚本仅支持单个关键字")
        self.word = Word
        self.char_table = {ord(key): ord(value) for key, value in Bai_duImgDownloader.char_table.items()}
        if not dir_path:
            dir_path = os.path.join(sys.path[0], 'results')
        self.dir_path = dir_path
        self.jsonUrlFile = os.path.join(sys.path[0], 'jsonUrl.txt')
        self.logFile = os.path.join(sys.path[0], 'logInfo.txt')
        self.errorFile = os.path.join(sys.path[0], 'errorUrl.txt')
        if os.path.exists(self.errorFile):
            os.remove(self.errorFile)
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        # 线程池
        self.pool = Pool(30)
        self.session = requests.Session()
        self.session.headers = Bai_duImgDownloader.headers
        self.queue = Queue()
        self.messageQueue = Queue()
        self.index = 0  # 图片起始编号，牵涉到计数，不要更改
        self.promptNum = 10  # 下载几张图片提示一次
        self.lock = threading.Lock()
        self.delay = 1.5  # 网络请求太频繁会被封
        self.QUIT = "QUIT"  # Queue中表示任务结束
        self.printPrefix = "**"  # 用于指定在控制台输出

    def start(self):
        # 控制台输出线程
        t = threading.Thread(target=self.__log)
        t.setDaemon(True)
        t.start()
        self.messageQueue.put(self.printPrefix + "脚本开始执行")
        start_time = dt.now()
        urls = self.__buildUrls()
        self.messageQueue.put(self.printPrefix + "已获取 %s 个Json请求网址" % len(urls))
        urls_ = int(input('请输入需要下载长度: '))
        # 解析出所有图片网址，该方法会阻塞直到任务完成
        self.pool.map(self.__resolveImgUrl, urls[0:urls_])
        while self.queue.qsize():
            images = self.queue.get()
            self.pool.map_async(self.__downImg, images)
        self.pool.close()
        self.pool.join()
        self.messageQueue.put(self.printPrefix + "下载完成！已下载 %s 张图片，总用时 %s" % (self.index, dt.now() - start_time))
        self.messageQueue.put(self.printPrefix + "请到 %s 查看结果！" % self.dir_path)
        self.messageQueue.put(self.printPrefix + "错误信息保存在 %s" % self.errorFile)
        self.messageQueue.put(self.QUIT)

    def __log(self):
        """控制台输出，加锁以免被多线程打乱"""
        with open(self.logFile, "w", encoding="utf-8") as f:
            while True:
                message = self.messageQueue.get()
                if message == self.QUIT:
                    break
                message = str(dt.now()) + " " + message
                if self.printPrefix in message:
                    print(message)
                elif "已下载" in message:
                    # 下载N张图片提示一次
                    downNum = self.re_downNum.findall(message)
                    if downNum and int(downNum[0]) % self.promptNum == 0:
                        print(message)
                f.write(message + '\n')
                f.flush()

    def __getIndex(self):
        """获取文件编号"""
        self.lock.acquire()
        try:
            return self.index
        finally:
            self.index += 1
            self.lock.release()

    def decode(self, url):
        """解码图片URL
        解码前：
        ippr_z2C$qAzdH3FAzdH3Ffl_z&e3Bftgwt42_z&e3BvgAzdH3F4omlaAzdH3Faa8W3ZyEpymRmx3Y1p7bb&mla
        解码后：
        http://s9.sinaimg.cn/mw690/001WjZyEty6R6xjYdtu88&690
        """
        # 先替换字符串
        for key, value in self.str_table.items():
            url = url.replace(key, value)
        # 再替换剩下的字符
        return url.translate(self.char_table)

    def __buildUrls(self):
        """json请求网址生成器"""
        words = parse.quote(self.word)
        url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}" \
              r"&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
        time.sleep(self.delay)
        # content 字节输出，返回的是一个字符串
        html = self.session.get(url.format(word=words, pn=0), timeout=15).content.decode('utf-8')
        # 获取这个网页的总图片数量
        results = re.findall(r'"displayNum":(\d+),', html)
        maxNum = int(results[0]) if results else 0
        # 所有请求网址network-XHR
        urls = [url.format(word=words, pn=x) for x in range(0, maxNum + 1, 60)]
        with open(self.jsonUrlFile, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")
        return urls

    def __resolveImgUrl(self, url):
        """从指定网页中解析出图片URL"""
        time.sleep(self.delay)
        html = self.session.get(url, timeout=15).content.decode('utf-8')
        # 查找出对应网页中objURL中的编码url和图片类型type
        data_s = self.re_objURL.findall(html)
        # img_s为一个对象列表
        img_s = [Image(self.decode(x[0]), x[1]) for x in data_s]
        self.messageQueue.put(self.printPrefix + "已解析出 %s 个图片网址" % len(img_s))
        self.queue.put(img_s)

    def __downImg(self, img):
        """下载单张图片，传入的是Image对象"""
        imgUrl = img.url
        message = 0
        res = 0
        try:
            time.sleep(self.delay)
            res = self.session.get(imgUrl, timeout=15)
            message = None
            if str(res.status_code)[0] == "4":
                message = "\n%s： %s" % (res.status_code, imgUrl)
            elif "text/html" in res.headers["Content-Type"]:
                message = "\n无法打开图片： %s" % imgUrl
        except Exception as e:
            message = "\n抛出异常： %s\n%s" % (imgUrl, str(e))
        finally:
            if message:
                self.messageQueue.put(message)
                self.__saveError(message)
                return
        index = self.__getIndex()
        # index从0开始
        self.messageQueue.put("已下载 %s 张图片：%s" % (index + 1, imgUrl))
        filename = os.path.join(self.dir_path, str(index) + "." + img.type)
        if img.type == 'gif':
            pass
        else:
            with open(filename, "wb") as f:
                f.write(res.content)

    def __saveError(self, mess_age):
        self.lock.acquire()
        try:
            with open(self.errorFile, "a", encoding="utf-8") as f:
                f.write(mess_age)
        finally:
            self.lock.release()


class Image(object):
    """图片类，保存图片信息"""
    def __init__(self, url, types):
        super(Image, self).__init__()
        self.url = url
        self.type = types


if __name__ == '__main__':
    print("欢迎使用百度图片下载脚本！\n目前仅支持单个关键词。")
    print("下载结果保存在脚本目录下的results文件夹中。")
    print("=" * 50)
    word = input("请输入你要下载的图片关键词：\n")
    Bai_duImgDownloader(word).start()
