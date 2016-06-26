# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def get_path(directory, prefix=None):
    if prefix is None:
        return "{}".format(directory)
    else:
        return "{}/{}".format(directory, prefix)


def change_directory(path, current_directory):
    if path.startswith("/"):
        current_directory = _update_directory(path, "")
    else:
        current_directory = _update_directory(path, current_directory)
    return current_directory


def _update_directory(path, directory):
    parsed_path = [p for p in path.split("/") if p != ""]
    parsed_dir = [d for d in directory.split("/") if d != ""]
    for p in parsed_path:
        if p == ".":
            continue
        if p == "..":
            parsed_dir = parsed_dir[:-1]
            continue
        parsed_dir.append(p)
    return "/".join(parsed_dir)
