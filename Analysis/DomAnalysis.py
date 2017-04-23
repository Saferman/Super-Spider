#encoding=utf-8
import re
import urllib
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
        self.soup = BeautifulSoup(dom, "lxml")  #self.soup内容默认是unicode
        self.url = url
        self.pattern = re.compile("href=([a-zA-Z0-9'\"+?=.%/_]*)")

    def _is_input_with_onclick(self,tag):
        return (tag.name == 'input') and (tag.get('type')=='button') and tag.has_attr('onclick')

    def ShowHTML(self):
        #https://www.crummy.com/software/BeautifulSoup/bs3/documentation.zh.html 发现prettify是u字符
        print self.soup.prettify().encode('utf-8','ignore')

    def GetURL(self):
        URL = []
        # 得到页面编码情况
        if not self.soup.meta.get('content'):
            if 'utf-8' in self.soup.meta.get('content'):
                charset = 'utf-8'
            else:
                charset = 'gbk'
        else:
            charset = 'utf-8'

        # 静态页面链接分析 和 javascript动态解析
        for tag in self.soup.find_all('a'):
            #print tag.get('href')
            if self.judge(tag.get('href')):
                URL.append(self.filter(tag.get('href')))
                #print self.filter(tag.get('href'))

        # 自动分析表单
        for tag in self.soup.find_all('form'):
            if not tag.get('action'):
                action_url = ''
            else:
                action_url = tag.get('action')
            action_url = self.filter(action_url)
            param = []
            for tag2 in tag.find_all('input'):
                if tag2.get('name') == None:
                        continue
                value = tag2.get('value').encode(charset,'ignore') 
                if not value:
                    value = 'admin' #以后再增加表单提交功能
                param.append(tag2.get('name')+'='+urllib.quote(value)) 
            URL.append(action_url + "?" + '&'.join(param))
        
        #  自动交互. 这里采用静态析的思路提取交互式生成的链接
        for tag in self.soup.find_all(self._is_input_with_onclick):
            for item in re.findall(self.pattern, tag.get('onclick')):
                URL.append(self.filter(self.onclick_filter(item)))

        # ajax请求









        
