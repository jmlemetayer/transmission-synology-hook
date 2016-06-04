#!/usr/bin/env python

import syslog
import transmission

def callback(relpath):
    print relpath

syslog.openlog("tr-syno-hook")

try:
    transmission.foreach(callback)
except Exception as e:
    syslog.syslog("Error: {}".format(e.args))

syslog.closelog()
