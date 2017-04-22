#encoding=utf-8
from bs4 import BeautifulSoup
from FilterURL import FilterURL
"""
Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种:
    Tag
    NavigableString
    BeautifulSoup
    Comment
"""

class DomAnalysis(FilterURL):

    def __init__(self, dom, url):
        self.soup = BeautifulSoup(dom, "lxml")
        self.url = url

    def ShowHTML(self):
        #https://www.crummy.com/software/BeautifulSoup/bs3/documentation.zh.html 发现prettify是u字符
        print self.soup.prettify().encode('utf-8','ignore')

    def GetURL(self):
        URL = []
        # 静态页面链接分析
        for tag in self.soup.find_all('a'):
            #print tag.get('href')
            if self.judge(tag.get('href')):
                #URL.append(self.filter(tag.get('href')))
                print self.filter(tag.get('href'))





        
