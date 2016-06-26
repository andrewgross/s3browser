# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def print_help(*args):
    GREEN = '\033[32m'
    END = '\033[0m'
    print('{color}{}{end} '.format(*args, color=GREEN, end=END))  # noqa


def color_yellow(text):
    YELLOW = '\033[33m'
    END = '\033[0m'
    return '{color}{text}{end}'.format(color=YELLOW, end=END, text=text)
