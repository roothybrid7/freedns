#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import traceback
import settings
import utils
import ConfigParser


class FreednsConfigParser(object):

    def __init__(self, filename=None):
        self.config = ConfigParser.ConfigParser()
        if filename:
            self.set_file(filename)

    def set_file(self, filename):
        self.filename = filename

    def add_section(self, section):
        if not self.config.has_section(section):
            self.config.add_section(section)
            return self
        else:
            return None

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


class FreednsConfigLoader(object):

    def __init__(self):
        self.load(settings)

    def load(self, settings=None):
        # Parameters for Option Parser
        self.options = settings.CMD_OPTIONS
        self.version = settings.VERSION
        # API Parameters
        self.params = settings.TARGET_PARAMS
        self.api = settings.TARGET_API
        self.hash = settings.HASH_ARGO
        self.timeout = settings.TIMEOUT

    def get(self, section, option):
        return self.config.get(section, option)

    def set(self, section, option, value):
        if self.config.has_section(section):
            self.config.set(section, option, value)
            return True
        else:
            return False

    def set_auth(self, username, password):
        import getpass
        # Get password from CommandLine
        if username:
            self.params[self.hash] = utils.gethashstr(
                username, password or getpass.getpass())
        elif password:
            self.params[self.hash] = utils.gethashstr(
                getpass.getuser(), password)
        # Read configfile
        else:
            cfg = FreednsConfigParser(settings.SECRET)
            cfg.read()
            self.params[self.hash] = cfg.get(settings.SECTION, self.hash)

    def get_request_url(self):

        query = ''
        for k, v in self.params.items():
            query += '?' if query == '' else '&'
            query += '{key}={value}'.format(key=k, value=v)

        return self.api + query


def main():

    from optparse import OptionParser
    import settings
    import getpass
    import utils

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
    hashstr = utils.gethashstr(username, password)

    config = FreednsConfigLoader(settings.SECRET)
    config.add_section(settings.SECTION)
    config.set(settings.SECTION, settings.HASH_ARGO, hashstr)
    config.write()

if __name__ == "__main__":
    main()
