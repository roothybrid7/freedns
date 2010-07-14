#!/usr/bin/env python
# -*- coding:utf-8 -*-
try:
    import settings
    import utils
except ImportError, e:
    import sys
    sys.stderr.write("Settings import error: " + e)
    sys.exit(1)


def getuserpass(username, password):

    # Read configfile
    if not any([username, password]):
        from loadconfig import FreednsConfigLoader
        loader = FreednsConfigLoader()
        loader.setfile(settings.SECRET)
        loader.read()
        return loader.get(settings.SECTION, settings.HASH_ARGO)

    import getpass
    # Get CommandLine
    if username:
        return utils.gethashstr(username, password or getpass.getpass())
    # Get ENV VARIABLE: LOGNAME > USER > LNAME > USERNAME
    else:
        return utils.gethashstr(getpass.getuser(), password)


def main():

    from optparse import OptionParser
    parser = OptionParser(option_list=settings.CMD_OPTIONS,
        version=settings.VERSION)

    options, args = parser.parse_args()
    settings.verbose(options.verbose)
    try:
        settings.TARGET_PARAMS[settings.HASH_ARGO] = getuserpass(
            options.username, options.password)
        res = utils.request(settings.TARGET_API,
            settings.TIMEOUT, **settings.TARGET_PARAMS)
        utils.update(res, settings.TIMEOUT)
    except Exception, e:
        parser.print_help()
        import sys
        sys.stderr.write(e)

if __name__ == "__main__":
    main()
