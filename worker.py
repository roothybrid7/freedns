#!/usr/bin/env python
# -*= coding:utf-8 -*-
import threading
import urllib2


class AsyncWorker(threading.Thread):
    def __init__(self, url, timeout):
        threading.Thread.__init__(self)
        self.url = url
        self.timeout = timeout

    def run(self):
        try:
            print 'Connecting URL: {url} ...'.format(url=self.url)
            res = urllib2.urlopen(url=self.url, timeout=self.timeout)
            return True
        except:
            return False
            raise
        else:
            print 'URL: {url} update successfully.'.format(url=self.url)
