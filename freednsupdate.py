#!/usr/bin/env python
# -*- coding:utf-8 -*-
try:
    import settings
    import utils
    import traceback
except ImportError, e:
    import sys
    sys.stderr.write("Settings import error: " + e)
    sys.exit(1)


def main():

    from optparse import OptionParser
    import getpass
    parser = OptionParser(option_list=settings.CMD_OPTIONS,
        version=settings.VERSION)

    options, args = parser.parse_args()
    if not options.verbose:
        import os, sys
        sys.stdout = open(os.devnull)
    try:
        # read configfile
        if not options.username and not options.password:
            from loadconfig import FreednsConfigLoader
            loader = FreednsConfigLoader()
            loader.setfile(settings.SECRET)
            loader.read()
            hashstr = loader.get(settings.SECTION, settings.HASH_ARGO)
        elif options.username:
            username = options.username
            password = options.password or getpass.getpass()
            hashstr = utils.gethashstr(username, password)
        elif options.password:
            # Get ENV VARIABLE: LOGNAME > USER > LNAME > USERNAME
            username = getpass.getuser()
            password = options.password
            hashstr = utils.gethashstr(username, password)

        settings.TARGET_PARAMS[settings.HASH_ARGO] = hashstr
        res = utils.request(settings.TARGET_API,
            settings.TIMEOUT, **settings.TARGET_PARAMS)
        utils.update(res, settings.TIMEOUT)
    except:
        traceback.print_stack()

if __name__ == "__main__":
    main()
