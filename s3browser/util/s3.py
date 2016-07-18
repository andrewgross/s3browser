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
