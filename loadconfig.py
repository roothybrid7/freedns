#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import traceback
import ConfigParser


class FreednsConfigLoader(object):

    def __init__(self):
        self.config = ConfigParser.ConfigParser()

    def setfile(self, filename):
        self.filename = filename

    def add_section(self, section):
        if not self.config.has_section(section):
            self.config.add_section(section)
            return True
        else:
            return False

    def get(self, section, option):
        return self.config.get(section, option)

    def set(self, section, option, value):
        if self.config.has_section(section):
            self.config.set(section, option, value)
            return True
        else:
            return False

    def write(self):
        try:
            if self.filename:
                with open(self.filename, 'wb') as f:
                    self.config.write(f)
                return True
            else:
                return False
        except:
            sys.stderr.write(traceback.format_exc())
            raise

    def read(self):
        try:
            if self.filename:
                self.config.read(self.filename)
                return True
            else:
                return False
        except:
            sys.stderr.write(traceback.format_exc())
            raise


def main():

    from optparse import OptionParser
    import settings
    import getpass

    parser = OptionParser()
    parser.add_option("-u", "--username", dest="username")
    parser.add_option("-p", "--password", dest="password")

    options, args = parser.parse_args()
    if not options.username:
        sys.stderr.write("Input username!!\n")
        parser.print_help()
        sys.exit(1)
    username = options.username
    password = options.password or getpass.getpass()
    hashstr = gethashstr(username, password)

    config = FreednsConfigLoader()
    config.add_section(settings.SECTION)
    config.set(settings.SECTION, settings.HASH_ARGO, hashstr)
    config.setfile(settings.SECRET)
    config.write()

if __name__ == "__main__":
    main()
