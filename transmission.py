#!/usr/bin/env python

import os

def foreach(callback):
    tdir = os.getenv('TR_TORRENT_DIR')
    assert tdir, "No torrent directory"
    tname = os.getenv('TR_TORRENT_NAME')
    assert tname, "No torrent name"
    tpath = os.path.join(tdir, tname)
    if os.path.isfile(tpath):
        callback(os.path.relpath(tpath, tdir))
    elif os.path.isdir(tpath):
        for troot, tdirs, tfiles in os.walk(tpath):
            for tfile in tfiles:
                callback(os.path.relpath(os.path.join(troot, tfile), tdir))
