def gethashstr(username, password):

    import hashlib

    hashobj = hashlib.sha1()
    encstr = '|'.join([username, password])
    hashobj.update(encstr)
    hashstring = hashobj.hexdigest()
    return hashstring

def request(url, timeout, **params):

    query = ''
    for k, v in params.items():
        query += '?' if query == '' else '&'
        query += '{key}={value}'.format(key=k, value=v)

    url += query

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

        # record update
        from worker import AsyncWorker
        tasks = []
        for u in urls:
            t = AsyncWorker(u.text, timeout)
            tasks.append(t)
            t.start()

        # wait for the background tasks to finish
        for t in tasks:
            t.join()
        print 'Dynamic dns update tasks were done.'
    except:
        raise
    finally:
        output.close()

