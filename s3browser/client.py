# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import cmd

from .util.list import parse_ls, print_files, complete_dir
from .util.path import change_directory, get_pwd
from .util.parsers import ls_parser
from .util.s3 import get_keys, get_buckets, get_bucket
from .util.tree import build_tree, S3Bucket, S3
from .helpers import print_help, print_result, color_green


# This makes mocking easier
get_input = raw_input


class S3Browser(cmd.Cmd, object):

    def __init__(self, connection):
        super(S3Browser, self).__init__()
        self.connection = connection
        self._top = S3("")
        self.current_directory = self._top
        self._get_all_buckets()
        self._update_prompt()

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

    def do_buckets(self, line):
        if line == "":
            for bucket in sorted(self._top.buckets):
                print bucket.name
        else:
            self.current_directory = self._top.get_child(line)

    def help_buckets(self):
        print_help("""usage: buckets [<bucket_name>]

Lists all known buckets or switches the current bucket to <bucket_name>
""")

    def complete_buckets(self, text, line, begidx, endidx):
        buckets = sorted(self._top.buckets)
        return [b.name for b in buckets if b.name.startswith(text)]

    def do_refresh(self, line):
        if line == "":
            print "Refreshing all buckets! Get a snickers."
            for bucket in self._top.dirs:
                print "Refreshing {}".format(bucket.name)
                self._refresh_bucket(bucket)
        else:
            bucket = self._top.get_child(line)
            if bucket is None:
                print "{} is not a valid bucket name!".format(line)
            self._refresh_bucket(bucket)
            self.current_directory = bucket

    def _refresh_bucket(self, bucket):
        build_tree(bucket, get_keys(get_bucket(bucket.name, self.connection), interactive=True))
        bucket.refreshed = True
        return bucket

    def complete_refresh(self, text, line, begidx, endidx):
        buckets = sorted(self._top.dirs)
        return [b.name for b in buckets if b.name.startswith(text)]

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
        if self.current_directory.name:
            self.prompt = '{} $ '.format(color_green(self.current_directory.name))
        else:
            self.prompt = '$ '

    def postcmd(self, stop, line):
        self._update_prompt()
        return stop

    do_EOF = do_exit

    def _get_all_buckets(self):
        print "Getting all buckets!"
        buckets = get_buckets(self.connection)
        for bucket in buckets:
            self._top.add_child(S3Bucket(bucket.name))
