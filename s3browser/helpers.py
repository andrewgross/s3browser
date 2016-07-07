# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import sys

# This makes mocking easier
output = sys.stdout
error = sys.stderr


def print_result(*args):
    print(*args, file=output)  # noqa


def print_help(*args):
    GREEN = '\033[32m'
    END = '\033[0m'
    print('{color}{}{end} '.format(*args, color=GREEN, end=END), file=error)  # noqa


def color_yellow(text):
    YELLOW = '\033[33m'
    END = '\033[0m'
    return '{color}{text}{end}'.format(color=YELLOW, end=END, text=text)


def color_blue(text):
    BLUE = '\033[34m'
    END = '\033[0m'
    return '{color}{text}{end}'.format(color=BLUE, end=END, text=text)


def color_green(text):
    GREEN = '\033[32m'
    END = '\033[0m'
    return '{color}{text}{end}'.format(color=GREEN, end=END, text=text)
