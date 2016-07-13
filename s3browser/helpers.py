# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import sys
import datetime

# This makes mocking easier
output = sys.stdout
error = sys.stderr

# Pretty Colors
WHITE = '\033[37m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
GREEN = '\033[32m'
END = '\033[0m'


def print_result(*args):
    print(*args, file=output)  # noqa


def print_help(*args):
    print('{color}{}{end} '.format(*args, color=WHITE, end=END), file=error)  # noqa


def color_yellow(text):
    return '{color}{text}{end}'.format(color=YELLOW, end=END, text=text)


def color_blue(text):
    return '{color}{text}{end}'.format(color=BLUE, end=END, text=text)


def color_green(text):
    return '{color}{text}{end}'.format(color=GREEN, end=END, text=text)


def convert_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
