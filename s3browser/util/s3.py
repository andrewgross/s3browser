# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import datetime

from boto.s3.connection import S3Connection


def get_connection(access_key_id=None, secret_access_key=None):
    return S3Connection(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)


def get_bucket(bucket, connection):
    return connection.get_bucket(bucket)


def get_buckets(connection):
    buckets = connection.get_all_buckets()
    all_buckets = [b for b in buckets]
    return all_buckets


def get_keys(bucket, interactive=False):
    """
    Get all keys, interactive adds some fancy graphics
    """
    key_count = 0
    counter, timer = _interactive(interactive=interactive, timer=datetime.datetime.min, key_count=key_count)
    for key in bucket:
        yield key
        counter, timer = _interactive(counter=counter, timer=timer, interactive=interactive, key_count=key_count)
        key_count += 1
    if interactive:
        print "\nDone!"


def _interactive(counter=0, timer=None, interactive=False, key_count=0):
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
        _print_progress_bar(counter, key_count)
        timer = now
    return counter, timer


def _get_ticker_string(counter, key_count):
    """
    Print out our message while keeping a constant width string
    """
    anti_counter = 10 - counter
    return "This can take a while.{}{} Keys Found: {}".format("." * counter, " " * anti_counter, key_count)


def _print_progress_bar(counter, key_count):
    """
    Print out a message overtop of the existing line
    """
    ticker = _get_ticker_string(counter, key_count)
    sys.stdout.write(ticker)
    sys.stdout.flush()
    sys.stdout.write("\b" * (len(ticker) + 1))  # Move back to the beginning of the line


def _check_time(now, timer):
    return (now - timer) > datetime.timedelta(seconds=1)
