#encoding=utf-8
import re

class FilterURL(object):

    def __init__(self):
        pass

    def judge(self, link):
        if link == None:
            return False
        if link == '/':
            return False
        if link.find('javascript:')==0:
            return False
        if link.find('http')!=-1 and link.find(self.url)==-1:
            # 去掉不在同源策略范围链接
            return False
        return True
        
    def filter(self, link):
        if link.find('http')!=0:
            return self.url.rstrip('/') + "/" + link.lstrip('/')
        else:
            return link

    def onclick_filter(self, link):
        link_pattern = re.compile("[\"'][ ]*\+[ ]*[\"']")
        return re.sub(link_pattern, '', link)


    def test(self):
        print self.url