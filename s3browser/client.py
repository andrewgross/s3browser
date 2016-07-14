# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import cmd

from .util.list import parse_ls, print_files, complete_dir
from .util.path import change_directory, get_pwd
from .util.parsers import ls_parser
from .util.s3 import get_keys
from .util.tree import build_tree
from .helpers import print_help, print_result, color_green


# This makes mocking easier
get_input = raw_input


class S3Browser(cmd.Cmd, object):

    def __init__(self, bucket, connection):
        super(S3Browser, self).__init__()
        self.bucket = bucket
        self.connection = connection
        self.current_directory = None
        self._update_prompt()
        self.keys = None

    def do_cd(self, line):
        node = change_directory(line, self.current_directory)
        if node:
            self.current_directory = node
        else:
            print_result("No such directory")

    def complete_cd(self, text, line, begidx, endidx):
        return complete_dir(self.current_directory, text)

    def help_cd(self):
        print_help("""usage: cd [dir]

Changes the current directory.
""")

    def do_refresh(self, line):
        self.current_directory = build_tree(self.bucket.name, get_keys(self.bucket, interactive=True))

    def help_refresh(self):
        print_help("""usage: refresh

Refreshes list of keys in an S3 Bucket and builds a directory tree. This can take a while.
""")

    def do_ls(self, line):
        args = parse_ls(line)
        if args is None:
            return
        print_files(self.current_directory, args)

    def do_ll(self, line):
        self.do_ls("-l -h {}".format(line))

    def help_ls(self):
        parser = ls_parser()
        parser.print_help()

    def do_pwd(self, line):
        print_result(get_pwd(self.current_directory))

    def help_pwd(self):
        print_help("""usage: pwd

Print the current directory
""")

    def do_exit(self, line):
        return True

    def help_exit(self):
        print_help("""usage: exit

Exit S3Browser
""")

    def _update_prompt(self):
        if self.current_directory:
            self.prompt = '{} $ '.format(color_green(self.current_directory.name))
        else:
            self.prompt = '{} $ '.format(color_green(self.bucket.name))

    def postcmd(self, stop, line):
        self._update_prompt()
        return stop

    do_EOF = do_exit
