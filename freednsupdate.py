#!/usr/bin/env python
# -*- coding:utf-8 -*-

__description__ = "Dynamic DNS update client for FreeDNS service"

__long_description__ = """
Description:

freednsupdate is a script for doing updates to FreeDNS of Dynamic DNS
Service.

Features:

- freednsupdate client uses FreeDNS API's and returns format xml.
- Because a standard function is used, an additional module need not be
  installed.

Example use::

    $ python freednsupdate.py -u hoge
    Password: <- Input user's password

Other:

Tested with python v2.6
"""

__copyright__ = """Copyright (c) 2010 Satoshi Ohki
"""

__author__ = "Satoshi Ohki"
__author_email__ = "@".join(("roothybrid7", "gmail.com"))
__license__ = "MIT License"
__version__ = "0.2.1"
__url__ = "http://github.com/satsv/freedns/"

# the following variable is useful when using setuptools or distutils
# (don't type things twice)
metadata = {
    'author': __author__,
    'author_email': __author_email__,
    'version': __version__,
    'license': __license__,
    'url': __url__,
    'description': __description__,
    'long_description': __long_description__,
    'copyright': __copyright__,
}


try:
    import utils
    from manage import FreednsConfigLoader
    from optparse import OptionParser
except ImportError, e:
    import sys
    sys.stderr.write("Modules import error: " + e)
    sys.exit(1)


def main():
    loader = FreednsConfigLoader()
    parser = OptionParser(
        option_list=loader.options, version=loader.version)
    (options, args) = parser.parse_args()
    try:
        loader.set_timeout(options.timeout)
        loader.set_auth(options.username, options.password)
        res = utils.request(loader.get_request_url(), loader.timeout)
        utils.update(res, loader.timeout)
    except Exception, e:
        import sys
        import traceback
        sys.stderr.write(traceback.format_exc())
        parser.print_help()

if __name__ == "__main__":
    main()
