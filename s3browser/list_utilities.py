# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .path_utilities import (
    get_path,
    get_relative_name,
    is_relative_file,
    is_relative_directory
)
from .parsers import ls_parser
from .helpers import color_blue


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
            last_modified = f.last_modified
            size = f.size
            print size, last_modified, name
    else:
        for f in sorted_files:
            name = get_relative_name(current_directory, f.name)
            is_dir = is_relative_directory(current_directory, f.name)
            if is_dir:
                name = color_blue(name)
            print name


def _sorted_files(files, ls_args):
    if ls_args.time:
        sorted_files = sort_files(files, key="last_modified", reverse=ls_args.reverse)
    elif ls_args.size:
        sorted_files = sort_files(files, key="size", reverse=ls_args.reverse)
    else:
        sorted_files = sort_files(files, reverse=ls_args.reverse)
    return sorted_files
