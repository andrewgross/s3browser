# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from s3browser.helpers import convert_date


class S3File(object):

    def __init__(self, name, size, last_modified, parent=None):
        self.name = name
        self._size = size
        self.parent = parent
        if isinstance(last_modified, datetime.datetime):
            self._last_modified = last_modified
        else:
            self._last_modified = convert_date(last_modified)

    def get_size(self):
        return self._size

    def get_last_modified(self):
        return self._last_modified

    def __repr__(self):
        return "{} - Size: {}  Last Modified: {}".format(self.name, self._size, self._last_modified)


class S3Dir(object):

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.files = []
        self.dirs = []
        self._size = 0
        self._last_modified = None

    def add_child(self, child):
        if isinstance(child, S3File):
            self.files.append(child)
        elif isinstance(child, S3Dir):
            self.dirs.append(child)
        else:
            raise "Attempted to add a bad child"
        child.parent = self

    def get_size(self):
        if not self._size:
            for f in self.files + self.dirs:
                self._size = self._size + f.get_size()
        return self._size

    def get_last_modified(self):
        if not self._last_modified:
            self._last_modified = datetime.datetime.min
            for f in self.files + self.dirs:
                if f.get_last_modified() > self._last_modified:
                    self._last_modified = f.get_last_modified()
        return self._last_modified

    def __repr__(self):
        return "{} - Files: {} Dirs: {}".format(self.name, len(self.files), len(self.dirs))


class S3Bucket(object):

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.files = []
        self.dirs = []
        self.refreshed = False
        self._size = 0
        self._last_modified = None

    def add_child(self, child):
        if isinstance(child, S3File):
            self.files.append(child)
        elif isinstance(child, S3Dir):
            self.dirs.append(child)
        else:
            raise "Attempted to add a bad child"
        child.parent = self

    def get_size(self):
        if not self.refreshed:
            return 0
        if not self._size:
            for f in self.files + self.dirs:
                self._size = self._size + f.get_size()
        return self._size

    def get_last_modified(self):
        if not self.refreshed:
            return datetime.date.min
        if not self._last_modified:
            self._last_modified = datetime.datetime.min
            for f in self.files + self.dirs:
                if f.get_last_modified() > self._last_modified:
                    self._last_modified = f.get_last_modified()
        return self._last_modified

    def __repr__(self):
        return "{} - Refreshed: {} - Files: {} Dirs: {}".format(self.name, self.refreshed, len(self.files), len(self.dirs))


class S3(object):

    def __init__(self, name):
        self.name = name
        self.dirs = []
        self.files = []
        self.size = 0
        self.parent = None
        self._last_modified = None

    def add_child(self, child):
        if isinstance(child, S3Bucket):
            self.dirs.append(child)
        else:
            raise "Attempted to add a bad child"
        child.parent = self

    def get_child(self, name):
        for bucket in self.dirs:
            if bucket.name == name:
                return bucket

    def get_size(self):
        if not self._size:
            for f in self.files + self.dirs:
                self._size = self._size + f.get_size()
        return self._size

    def get_last_modified(self):
        if not self._last_modified:
            self._last_modified = datetime.datetime.min
            for f in self.files + self.dirs:
                if f.get_last_modified() > self._last_modified:
                    self._last_modified = f.get_last_modified()
        return self._last_modified

    def __repr__(self):
        return "Top Level of S3"


def add_key(node, key, partial_name):
    split_name = partial_name.split("/")
    if partial_name == "":
        return
    elif len(split_name) == 1 and split_name != "":
        f = S3File(partial_name, key.size, key.last_modified)
        node.add_child(f)
    else:
        dir_name = split_name[0]
        new_dir = S3Dir(dir_name)
        new_name = partial_name[len(dir_name) + 1:]
        for d in node.dirs:
            if d.name == dir_name:
                return add_key(d, key, new_name)
        node.add_child(new_dir)
        add_key(new_dir, key, new_name)


def build_tree(base_node, keys):
    for key in keys:
        add_key(base_node, key, key.name)
    return base_node
