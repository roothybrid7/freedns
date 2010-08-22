#!/usr/bin/env python
# -*= coding:utf-8 -*-
import threading
from multiprocessing import Process
import urllib2


class AsyncWorker(Process):
    def __init__(self, url, timeout):
        Process.__init__(self)
        self.url = url
        self.timeout = timeout

    def run(self):
        try:
            print 'Connecting URL: {url} ...'.format(url=self.url)
            res = urllib2.urlopen(url=self.url, timeout=self.timeout)
        except:
            return False
            raise
        else:
            print 'URL: {url} update successfully.'.format(url=self.url)
            return True
