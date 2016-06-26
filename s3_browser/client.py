# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import cmd
import sys
import functools

from time import sleep

from path_utilities import change_directory


# This makes mocking easier
get_input = raw_input


class S3Browser(cmd.Cmd, object):

    def __init__(self, bucket, connection):
        super(S3Browser, self).__init__()
        self.bucket = bucket
        self.connection = connection
        self.current_directory = ""
        self.prompt = '{}$ '.format(self.current_directory)

    def do_cd(self, line):
        self.current_directory = change_directory(line, self.current_directory)

    def complete_cd(self, text, line, begidx, endidx):
        return []

    def help_cd(self):
        print_help("""
cd

Changes the current directory.""")

    def do_exit(self, line):
        return True

    def help_exit(self):
        print_help("""
exit

Exit S3Browser""")

    do_EOF = do_exit


    def _update_prompt(self):
        if self.current_directory:
            self.prompt = '{} $ '.format(print_yellow(self.current_directory))
        else:
            self.prompt = '$ '


    def postcmd(stop, line):
        _update_prompt()


def print_yellow(text):
    YELLOW = '\033[33m'
    END = '\033[0m'
    return '{color}{text}{end}'.format(color=YELLOW, end=END, text=text)
