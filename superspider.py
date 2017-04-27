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
from downloader import Crawler
from DuplicateRemoval.DuplicateRemoval import Duplicate
import hashlib
from PyQt4.QtGui import QApplication

def MD5(s):
    m = hashlib.md5() 
    m.update(s)
    return m.hexdigest()

class Spider(object):

    def __init__(self, url):
        url = self._normalize(url)
        self.tasks = [url]
        self.check_urls = []
        self.ID = [0]
        self.conn = self._connectDB(url)

    def _normalize(self, url):   
        # 域名前的要正规，末尾要有/
        url = url.rstrip('/') + '/'
        if url.find(':')!=-1:
            url = url[0:url.find(':')+1].lower() + '//' + url[url.find(':')+1:].lstrip('/')
        return url

    def _isend(self):
        if not self.tasks:
            return True
        else:
            return False

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
        app = QApplication(sys.argv)
        while not self._isend():
            for u in self.tasks:
                print u
            crawler = Crawler(app, self.check_urls)
            crawler.start(self.tasks)
            app.exec_()
            self.tasks = []
            for u in self.check_urls:
                if not Duplicate(self.conn, self.ID, u):
                    self.tasks.append(u)
                else:
                    pass
            self.check_urls = []
        print "[+]End"

    def execute(self):
        self.pagecrawl()
        self.conn.close()

if __name__ == '__main__':
    Spider_url = "http://demo.aisec.cn/demo/aisec/"
    Spider(Spider_url).execute()