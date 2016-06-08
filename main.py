#!/usr/bin/env python

import os
import synology
import syslog
import transmission
import urlparse
import yaml

syslog.openlog('tr-syno-hook')

try:
    top = os.path.dirname(os.path.realpath(__file__))
    config = yaml.safe_load(open(os.path.join(top, 'config.yml')))

    def create_tree(relpath, tree):
        directory = os.path.dirname(relpath)
        url = urlparse.urljoin(config['webshare']['url'], relpath)
        if not any(dir['name'] == directory for dir in tree):
            dir = dict()
            dir['name'] = directory
            dir['urls'] = list()
            dir['urls'].append(url)
            tree.append(dir)
        else:
            dir = next(dir for dir in tree if dir['name'] == directory)
            dir['urls'].append(url)

    tree = list()
    transmission.foreach(create_tree, tree)
    syno = synology.synology(config['synology']['url'])
    syno.login(config['synology']['username'], config['synology']['password'])
    for dir in tree:
        dest = os.path.join(config['synology']['destination'], dir['name'])
        for url in dir['urls']:
            syslog.syslog('"{}" <- "{}"'.format(dest, url))
        if dir['name']:
            syno.mkdir(config['synology']['destination'], dir['name'])
        syno.download(dir['urls'], dest, \
                config['webshare']['username'], config['webshare']['password'])
    syno.logout()
except Exception as e:
    syslog.syslog('Error: {}'.format(e.args))

syslog.closelog()
