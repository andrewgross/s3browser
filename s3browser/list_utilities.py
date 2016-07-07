# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .path_utilities import (
    get_path,
    get_relative_name,
    is_relative_file,
    is_relative_directory
)
from .parsers import ls_parser


def get_matches(current_directory, files, prefix=None):
    path = get_path(current_directory, prefix=prefix)
    return filter(lambda x: x.name.startswith(path), files)


def sort_files(files, key="name"):
    return sorted(files, key=lambda x: getattr(x, key))


def get_names(files):
    return map(lambda x: x.name, files)


def get_sub_directory_names(current_directory, files):
    relative_dirs = filter(lambda x: is_relative_directory(current_directory, x.name), files)
    return map(lambda x: get_relative_name(current_directory, x.name), relative_dirs)


def get_sub_file_names(current_directory, files):
    relative_files = filter(lambda x: is_relative_file(current_directory, x.name), files)
    return map(lambda x: get_relative_name(current_directory, x.name), relative_files)


def get_files(current_directory, keys):
    return sort_files(get_matches(current_directory, keys))


def parse_ls(line):
    parser = ls_parser()
    try:
        args = parser.parse_args(line.split(" "))
    except SystemExit:
        args = None
    return args
