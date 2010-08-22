def gethashstr(username, password):
    import hashlib

    hashobj = hashlib.sha1()
    encstr = '|'.join([username, password])
    hashobj.update(encstr)
    hashstring = hashobj.hexdigest()
    return hashstring


def request(url, timeout):
    import urllib2

    print 'Connecting URL: {url} ...'.format(url=url)
    res = urllib2.urlopen(url=url, timeout=timeout)
    print 'URL: {url} contents download finished.'.format(url=url)
    responsetext = res.read()
    return responsetext


# Update the dynamic dns records using API
def update(responsetext, timeout):
    from xml.etree.ElementTree import ElementTree
    from StringIO import StringIO

    try:
        # xml.etree.ElementTree requires FileObject
        output = StringIO(responsetext)
        tree = ElementTree()
        tree.parse(output)
        urls = tree.findall("item/url")

        # Record update
        from worker import AsyncWorker
        tasks = [AsyncWorker(u.text, timeout) for u in urls]
        for t in tasks:
            t.start()

        # wait for the background tasks to finish
        for t in tasks:
            t.join()
        print 'Dynamic dns update tasks has finished.'
    except:
        raise
    finally:
        output.close()
