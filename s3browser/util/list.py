# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from s3browser.util.parsers import ls_parser
from s3browser.util.s3 import S3Dir
from s3browser.helpers import color_blue, print_result


def sort_files(files, key="name", reverse=False):
    if key == "last_modified":
        return sorted(files, key=lambda x: x.get_last_modified(), reverse=reverse)
    elif key == "size":
        return sorted(files, key=lambda x: x.get_size(), reverse=reverse)
    else:
        return sorted(files, key=lambda x: getattr(x, key), reverse=reverse)


def get_names(files):
    return map(lambda x: x.name, files)


def parse_ls(line):
    parser = ls_parser()
    try:
        args = parser.parse_args(line.split(" "))
    except SystemExit:
        args = None
    return args


def complete_dir(current_directory, prefix):
    dirs = sort_files(current_directory.dirs)
    return [d.name for d in dirs if d.name.startswith(prefix)]


def print_files(current_directory, ls_args):
    files = current_directory.dirs + current_directory.files
    sorted_files = _sorted_files(files, ls_args)
    for f in sorted_files:
        name = f.name
        last_modified = _format_date(f.get_last_modified())
        size = _format_size(f.get_size(), human=ls_args.human)
        is_dir = _is_dir(f)
        if is_dir:
            name = color_blue(name)
        if ls_args.long:
            print_result(size, last_modified, name)
        else:
            print_result(name)


def _is_dir(file):
    if isinstance(file, S3Dir):
        return True
    return False


def _sorted_files(files, ls_args):
    if ls_args.time:
        sorted_files = sort_files(files, key="last_modified", reverse=ls_args.reverse)
    elif ls_args.size:
        sorted_files = sort_files(files, key="size", reverse=ls_args.reverse)
    else:
        sorted_files = sort_files(files, reverse=ls_args.reverse)
    return sorted_files


def _format_date(date):
    """
    Converts a python datetime to a string
    """
    return date.strftime("%Y-%m-%d %H:%M")


def _format_size(size, human=False):
    if not human:
        return "{:>15}B".format(size)
    billion = 1024 * 1024 * 1024
    million = 1024 * 1024
    thousand = 1024
    if size >= billion:
        return "{:>4}G".format(size / billion)
    elif size >= million:
        return "{:>4}M".format(size / million)
    elif size >= thousand:
        return "{:>4}K".format(size / thousand)
    else:
        return "{:>4}B".format(size)
