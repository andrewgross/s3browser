# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from s3browser.util.path import (
    get_path,
    get_relative_name,
    is_relative_file,
    is_relative_directory
)
from s3browser.util.parsers import ls_parser
from s3browser.helpers import color_blue, print_result


def get_matches(current_directory, files, prefix=None):
    path = get_path(current_directory, prefix=prefix)
    return filter(lambda x: x.name.startswith(path), files)


def sort_files(files, key="name", reverse=False):
    return sorted(files, key=lambda x: getattr(x, key), reverse=reverse)


def get_names(files):
    return map(lambda x: x.name, files)


def get_sub_directory_names(current_directory, files):
    relative_dirs = filter(lambda x: is_relative_directory(current_directory, x.name), files)
    return map(lambda x: get_relative_name(current_directory, x.name), relative_dirs)


def get_sub_file_names(current_directory, files):
    relative_files = filter(lambda x: is_relative_file(current_directory, x.name), files)
    return map(lambda x: get_relative_name(current_directory, x.name), relative_files)


def parse_ls(line):
    parser = ls_parser()
    try:
        args = parser.parse_args(line.split(" "))
    except SystemExit:
        args = None
    return args


def print_files(current_directory, files, ls_args):
    sorted_files = _sorted_files(files, ls_args)
    if ls_args.long:
        for f in sorted_files:
            name = get_relative_name(current_directory, f.name)
            is_dir = is_relative_directory(current_directory, f.name)
            if is_dir:
                name = color_blue(name)
            last_modified = _format_date(f.last_modified)
            if ls_args.human:
                size = _format_size(f.size)
            else:
                size = f.size
            print_result(size, last_modified, name)
    else:
        for f in sorted_files:
            name = get_relative_name(current_directory, f.name)
            is_dir = is_relative_directory(current_directory, f.name)
            if is_dir:
                name = color_blue(name)
            print_result(name)


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
    Converts a python datetime string to a string
    """
    dt = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z")
    return dt.strftime("%Y-%m-%d %H:%M")


def _format_size(size):
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
