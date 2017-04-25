#encoding=utf-8
import re
import os
import sys
import time
import Queue
import urllib
import sqlite3
import requests
import threading
from downloader import Browser
from DuplicateRemoval.DuplicateRemoval import Duplicate
import hashlib

def MD5(s):
    m = hashlib.md5() 
    m.update(s)
    return m.hexdigest()

class Spider(object):

    def __init__(self, url):
        self.tasks = Queue.Queue()
        url = self._normalize(url)
        self.tasks.put(url)
        self.check = Queue.Queue()
        self.ID = [0]
        self.conn = self._connectDB(url)
        self.end_flag = 0
        self.threads_count = 1

    def _normalize(self, url):   
        return url

    def _check(self):
        while self.end_flag < self.threads_count:
            if not self.check.empty():
                check_url = self.check.get()    
                if Duplicate(self.conn, self.ID, check_url):
                    pass
                else:
                    self.tasks.put(check_url)
            else:
                pass

    def _connectDB(self,url):
        filename = MD5(url)
        if os.path.exists("./db/"+filename+".db3"):
            os.remove(("./db/"+filename+".db3").decode('UTF-8').encode('GBK'))
        else:
            pass
        conn = sqlite3.connect("./db/"+filename+".db3", check_same_thread=False)
        conn.execute('''CREATE TABLE URLS 
            (ID INT PRIMARY KEY  NOT NULL,
            URL TEXT       NOT NULL,
            MD5 TEXT       NOT NULL);''')
        print "[+]DB created successfully"
        return conn

    def pagecrawl(self):
        kong = 0
        while kong <= 5:
            if not self.tasks.empty():
                url = self.tasks.get()
                print "[+]pagecrawl:" + url
                for u in Browser(url).get_result():
                    self.check.put(u)
            else:
                kong += kong
                time.sleep(kong)
        self.end_flag += 1

    def execute(self):
        threads_count = self.threads_count
        threads = []
        for i in xrange(threads_count):
            t = threading.Thread(target=self.pagecrawl, args=())
            threads.append(t)
        for t in threads:
            t.setDaemon(True)
            t.start()
        self._check()
        self.conn.close()

if __name__ == '__main__':
    Spider("http://demo.aisec.cn/demo/aisec/").execute()