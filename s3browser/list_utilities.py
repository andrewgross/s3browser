# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .path_utilities import get_path


def get_matches(current_directory, files, prefix=None):
    path = get_path(current_directory, prefix=prefix)
    return filter(lambda x: x.name.startswith(path), files)


def sort_files(files):
    return sorted(files, key=lambda x: x.name)


def get_names(files):
    return map(lambda x: x.name, files)


def get_sub_directory_names(current_directory, files):
    directories = []
    for f in files:
        if _is_valid_directory(f.name, current_directory):
            remaining_string = f.name[len(current_directory):]
            if remaining_string.startswith("/"):
                remaining_string = remaining_string[1:]
            if "/" in remaining_string:
                directories.append(remaining_string.split("/")[0])
    return directories


def _is_valid_directory(filename, path):
    if filename.startswith(path):
        remaining_string = filename[len(path):]
        if "/" in remaining_string:
            return True
    return False
