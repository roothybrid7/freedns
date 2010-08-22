#!/usr/bin/env python
# -*- coding:utf-8 -*-
try:
    import utils
    from manage import FreednsConfigLoader
except ImportError, e:
    import sys
    sys.stderr.write("Modules import error: " + e)
    sys.exit(1)


def main():
    from optparse import OptionParser
    loader = FreednsConfigLoader()
    parser = OptionParser(
        option_list=loader.options, version=loader.version)
    (options, args) = parser.parse_args()
    try:
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
