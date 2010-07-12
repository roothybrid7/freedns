#!/usr/bin/env python
# -*= coding:utf-8 -*-
import threading
import urllib2

class AsyncWorker(threading.Thread) :
    def __init__(self, url, timeout):
        threading.Thread.__init__(self)
        self.url = url
        self.timeout = timeout
    def run(self) :
        print 'Connecting URL: {url} ...'.format(url=self.url)
        try:
            res = urllib2.urlopen(url=self.url, timeout=self.timeout)
        except:
            raise
        print 'URL: {url} update successfully.'.format(url=self.url)

