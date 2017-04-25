#encoding=utf-8
import sys
from functools import partial
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView, QWebSettings
from Analysis.DomAnalysis import DomAnalysis

class Crawler(object):

    def __init__(self, app):
        self.app = app
        self.root_url = ''
        self.result = []
        self.browsers = dict()

    def _load_finished(self, browser_id, ok):
        #print ok, browser_id
        web_view, _flag = self.browsers[browser_id]
        self.browsers[browser_id] = (web_view, True)

        frame = web_view.page().mainFrame()
        dom = unicode(frame.toHtml()).encode('utf-8','ignore')
        self.result += parse(dom, self.root_url)

        web_view.loadFinished.disconnect()
        web_view.stop()

        if all([closed for bid, closed in self.browsers.values()]):
            #print 'all finished'
            #for u in self.result:
            #    print u
            self.app.quit()

    def start(self, urls):
        for browser_id, url in enumerate(urls):
            self.root_url = url
            web_view = QWebView()
            web_view.settings().setAttribute(QWebSettings.AutoLoadImages,
                                             False)
            loaded = partial(self._load_finished, browser_id)
            web_view.loadFinished.connect(loaded)
            web_view.load(QUrl(url))
            self.browsers[browser_id] = (web_view, False)

def parse(dom, url):
    DomHandle = DomAnalysis(dom, url)
    return DomHandle.GetURL()


if __name__ == '__main__':
    url = ["http://demo.aisec.cn/demo/aisec/"]  
    app = QApplication(sys.argv)
    crawler = Crawler(app)
    crawler.start(url)
    app.exec_()


