# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import cmd

from .list_utilities import sort_files, get_matches, get_sub_directory_names, parse_ls, print_files
from .path_utilities import change_directory
from .s3_utilities import get_keys
from .helpers import print_help, print_result, color_yellow, color_green

# This makes mocking easier
get_input = raw_input


class S3Browser(cmd.Cmd, object):

    def __init__(self, bucket, connection):
        super(S3Browser, self).__init__()
        self.bucket = bucket
        self.connection = connection
        self.current_directory = ""
        self._update_prompt()
        self.keys = None

    def do_cd(self, line):
        self.current_directory = change_directory(line, self.current_directory)

    def complete_cd(self, text, line, begidx, endidx):
        return get_sub_directory_names(
            self.current_directory,
            sort_files(
                get_matches(
                    self.current_directory,
                    self.keys, prefix=text
                )
            )
        )

    def help_cd(self):
        print_help("""
cd

Changes the current directory.
""")

    def do_refresh(self, line):
        self.keys = get_keys(self.bucket, interactive=True)

    def help_refresh(self):
        print_help("""
refresh

Refreshes list of keys in an S3 Bucket. This can take a while.
""")

    def do_ls(self, line):
        args = parse_ls(line)
        if args is None:
            return
        matching_files = get_matches(self.current_directory, self.keys)
        print_files(self.current_directory, matching_files, args)

    def help_ls(self):
        print_help("""
ls

Lists files in the current directory
""")

    def do_pwd(self, line):
        print_result(self.current_directory)

    def help_pwd(self):
        print_help("""
pwd

Print the current directory
""")

    def do_exit(self, line):
        return True

    def help_exit(self):
        print_help("""
exit

Exit S3Browser
""")

    def _update_prompt(self):
        if self.current_directory:
            self.prompt = '{}:{} $ '.format(color_green(self.bucket.name), color_yellow(self.current_directory))
        else:
            self.prompt = '{}:{} $ '.format(color_green(self.bucket.name), color_yellow("~"))

    def postcmd(self, stop, line):
        self._update_prompt()
        return stop

    do_EOF = do_exit
