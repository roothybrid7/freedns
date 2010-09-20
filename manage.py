#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import traceback
import settings
import utils
import ConfigParser
import getpass
import logging


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
            return self
        else:
            return None

    def write(self):
        try:
            if self.filename:
                with open(self.filename, 'wb') as f:
                    self.config.write(f)
                return self
            else:
                return None
        except Exception, e:
            raise e

    def read(self):
        try:
            if self.filename:
                self.config.read(self.filename)
                return self
            else:
                return None
        except Exception, e:
            raise e


class FreednsConfigLoader(object):

    def __init__(self):
        self.__load(settings)

    def __load(self, settings=None):
        # Auth file parameters
        self.secfile = settings.SECRET
        self.section = settings.SECTION
        # Parameters for Option Parser
        self.options = settings.CMD_OPTIONS
        self.version = settings.VERSION
        # API Parameters
        self.params = settings.TARGET_PARAMS
        self.api = settings.TARGET_API
        self.hash = settings.HASH_ARGO
        self.timeout = settings.TIMEOUT
        # TODO: Logging
#        logging.baseConfig(
#            level=logging.DEBUG if settings.DEBUG else logging.WARNING,
#            format='%(name)-12s %(levelname)-8s %(messages)s')

    def set_timeout(self, timeout=None):
        if timeout is None:
            return self
        timeout = 1 if timeout < 1 else timeout
        self.timeout = timeout
        return self

    def set_auth(self, username, password):
        # Get password from CommandLine
        try:
            if username:
                self.params[self.hash] = utils.gethashstr(
                    username, password or getpass.getpass())
            elif password:
                self.params[self.hash] = utils.gethashstr(
                    getpass.getuser(), password)
            # Read configfile
            else:
                cfg = FreednsConfigParser(self.secfile)
                cfg.read()
                self.params[self.hash] = cfg.get(self.section, self.hash)
        except Exception, e:
            raise e
        return self

    def get_request_url(self):
        query = ''
        for k, v in self.params.items():
            query += '?' if query == '' else '&'
            query += '{key}={value}'.format(key=k, value=v)

        return self.api + query

    def create_authfile(self):
        try:
            cfg = FreednsConfigParser(self.secfile)
            cfg.add_section(self.section)
            cfg.set(self.section, self.hash, self.params[self.hash])
            cfg.write()
        except Exception, e:
            raise e
        return True


def create_authfile():
    if not options.username:
        parser.error("requires username")
        sys.exit(1)
    try:
        loader = FreednsConfigLoader()
        loader.set_auth(options.username, options.password)
        loader.create_authfile()
    except Exception, e:
        sys.stderr.write(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    from optparse import OptionParser

    usage = "usage: %prog create_authfile [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--username", dest="username")
    parser.add_option("-p", "--password", dest="password")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("requires argument of function name")
        sys.exit(1)
    if args[0] == 'create_authfile':
        create_authfile()
        print "Create authfile is successfully."
