#encoding=utf-8
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView
from Analysis.DomAnalysis import DomAnalysis

class Browser(QWebView):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)
        self.load(QUrl(url))
        self.app.exec_()

    def _result_available(self, ok):
        frame = self.page().mainFrame()
        #print unicode(frame.toHtml()).encode('utf-8')
        dom = unicode(frame.toHtml()).encode('utf-8','ignore')
        parse(dom, url)
        self.app.quit()

def parse(dom, url):
    DomHandle = DomAnalysis(dom, url)
    DomHandle.GetURL()


if __name__ == '__main__':
    url = "http://demo.aisec.cn/demo/aisec/"
    Browser(url)
    #print "[+]Over"
