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
    collapsed_files, filenames = _collapsed_files(sorted_files, current_directory)
    for filename in filenames:
        name = get_relative_name(current_directory, filename)
        is_dir = _is_dir(current_directory, filename, collapsed_files)
        if is_dir:
            name = color_blue(name)
        last_modified = _format_date(_get_date(filename, collapsed_files))
        size = _get_size(filename, collapsed_files)
        size = _format_size(size, human=ls_args.human)
        if ls_args.long:
            print_result(size, last_modified, name)
        else:
            print_result(name)


def _is_dir(current_directory, filename, collapsed_files):
    files = collapsed_files.get(filename, [])
    for f in files:
        if is_relative_directory(current_directory, f.name):
            return True
    return False


def _collapsed_files(files, current_directory):
    f_set = set()
    filenames = []
    grouped_files = {}
    for f in files:
        name = get_relative_name(current_directory, f.name)
        if name not in f_set:
            filenames.append(name)
            f_set.add(name)
        if grouped_files.get(name):
            grouped_files[name].append(f)
        else:
            grouped_files[name] = [f]
    return grouped_files, filenames


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


def _get_date(filename, collapsed_files):
    last_modified = datetime.datetime.min
    for f in collapsed_files[filename]:
        dt = datetime.datetime.strptime(f.last_modified, "%Y-%m-%dT%H:%M:%S.%fZ")
        if dt > last_modified:
            last_modified = dt
    return last_modified


def _get_size(filename, collapsed_files):
    total_size = 0
    for f in collapsed_files[filename]:
        total_size = total_size + f.size
    return total_size


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
