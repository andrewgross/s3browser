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
