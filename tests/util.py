# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import boto
import datetime

from boto.s3.key import Key

now = datetime.datetime.now()


class S3File(object):

    def __init__(self, name, last_modified=now, size=1):
        self.name = name
        self.last_modified = last_modified
        self.size = size


def get_unsorted_list_of_files(prefix=None):
    if prefix:
        _prefix = "{}/".format(prefix)
    else:
        _prefix = ""
    a = S3File(_prefix + "a", datetime.datetime.now())
    b = S3File(_prefix + "b", datetime.datetime.now() - datetime.timedelta(hours=1))
    c = S3File(_prefix + "c", datetime.datetime.now() - datetime.timedelta(hours=2))

    return [b, a, c]


def populate_bucket(bucket_name, keys):
    conn = boto.connect_s3()
    conn.create_bucket(bucket_name)
    bucket = conn.get_bucket(bucket_name)
    for key in keys:
        k = Key(bucket)
        k.key = key
        k.set_contents_from_string(key)
    return bucket, conn
