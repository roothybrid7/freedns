#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Debug mode
DEBUG = False

# User account and api settings
SECRET = os.path.join(BASE_DIR, ".freednssec.cfg")
SECTION = "Secret"
HASH_ARGO = "sha"
TARGET_PARAMS = {'action': "getdyndns", HASH_ARGO: None, 'style': "xml"}
TARGET_API = "http://freedns.afraid.org/api/"
TIMEOUT = 300

# Command Options
VERSION = "%prog 0.2.1"

from optparse import make_option
CMD_OPTIONS = [
    make_option("-u", "--user", dest="username",
        help="Username of FreeDNS domain hosting"),
    make_option("-p", "--pass", dest="password",
        help="User password of FreeDNS domain hosting"),
    make_option("-t", "--timeout", dest="timeout", type="int",
        help="""Access to FreeDNS API's in time(min value 1)
        [default: %default]""", default=TIMEOUT),
]
