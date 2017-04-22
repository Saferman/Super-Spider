#encoding=utf-8

class FilterURL(object):

    def __init__(self):
        pass

    def judge(self, link):
        if link == '/':
            return False
        if link.find('javascript:')==0:
            return False
        return True
        
    def filter(self, link):
        if link.find('http')!=0:
            return self.url + "/" + link.lstrip('/')
        else:
            return link

    def test(self):
        print self.url