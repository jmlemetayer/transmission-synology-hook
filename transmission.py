#!/usr/bin/env python

import os

def foreach(callback, args=None):
    directory = os.getenv('TR_TORRENT_DIR')
    assert directory, "No torrent directory"
    name = os.getenv('TR_TORRENT_NAME')
    assert name, "No torrent name"
    path = os.path.join(directory, name)
    if os.path.isfile(path):
        relpath = os.path.relpath(path, directory)
        callback(relpath, args)
    elif os.path.isdir(path):
        for root, directories, files in os.walk(path):
            for file in files:
                relpath = os.path.relpath(os.path.join(root, file), directory)
                callback(relpath, args)
