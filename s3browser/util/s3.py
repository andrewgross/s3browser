# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import datetime

from s3browser.helpers import convert_date

from boto.s3.connection import S3Connection


def get_connection(access_key_id=None, secret_access_key=None):
    return S3Connection(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)


def get_bucket(bucket, connection):
    return connection.get_bucket(bucket)


def get_keys(bucket, interactive=False):
    """
    Get all keys, interactive adds some fancy graphics
    """
    all_keys = []
    counter, timer = _interactive(interactive=interactive)
    for key in bucket:
        all_keys.append(key)
        counter, timer = _interactive(counter=counter, timer=timer, interactive=interactive)
    if interactive:
        print "\nDone!"
    return all_keys


def _interactive(counter=0, timer=None, interactive=False):
    """
    Print a status banner, adding a . every second, resetting at 10
    """
    now = datetime.datetime.now()
    if timer is None:
        timer = now
    after_one_second = _check_time(now, timer)
    if after_one_second and interactive:
        counter += 1
        counter = counter % 10
        _print_progress_bar(counter)
        timer = now
    return counter, timer


def _get_ticker_string(counter):
    """
    Print out our message while keeping a constant width string
    """
    anti_counter = 10 - counter
    return "This can take a while.{}{}".format("." * counter, " " * anti_counter)


def _print_progress_bar(counter):
    """
    Print out a message overtop of the existing line
    """
    ticker = _get_ticker_string(counter)
    sys.stdout.write(ticker)
    sys.stdout.flush()
    sys.stdout.write("\b" * (len(ticker) + 1))  # Move back to the beginning of the line


def _check_time(now, timer):
    return (now - timer) > datetime.timedelta(seconds=1)


class S3File(object):

    def __init__(self, name, size, last_modified):
        self.name = name
        self._size = size
        if isinstance(last_modified, datetime.datetime):
            self._last_modified = last_modified
        else:
            self._last_modified = convert_date(last_modified)

    def get_size(self):
        return self._size

    def get_last_modified(self):
        return self._last_modified


class S3Dir(object):

    def __init__(self, name):
        self.name = name
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
