#!/usr/bin/env python
# -*- coding:utf-8 -*-
try:
    import settings
    import utils
except ImportError, e:
    import sys
    sys.stderr.write("Settings import error: " + e)
    sys.exit(1)


def main():
    from loadconfig import FreednsConfigLoader
    from optparse import OptionParser
    loader = FreednsConfigLoader()
    parser = OptionParser(
        option_list=loader.options, version=loader.version)
    options, args = parser.parse_args()
    try:
        loader.set_auth(options.username, options.password)
        res = utils.request(loader.get_request_url(), loader.timeout)
        utils.update(res, loader.timeout)
    except Exception, e:
        parser.print_help()
        import sys
        sys.stderr.write(e)

if __name__ == "__main__":
    main()
