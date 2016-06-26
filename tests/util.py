# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime


class S3File(object):

    def __init__(self, name, last_modified):
        self.name = name
        self.last_modified = last_modified


def get_unsorted_list_of_files(prefix=None):
    if prefix:
        _prefix = "{}/".format(prefix)
    else:
        _prefix = ""
    a = S3File(_prefix + "a", datetime.datetime.now())
    b = S3File(_prefix + "b", datetime.datetime.now() - datetime.timedelta(hours=1))
    c = S3File(_prefix + "c", datetime.datetime.now() - datetime.timedelta(hours=2))

    return [b, a, c]
