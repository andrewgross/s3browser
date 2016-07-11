# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def get_path(directory, prefix=None):
    if prefix is None:
        return "{}".format(directory)
    if not directory:
        return "{}".format(prefix)
    else:
        return "{}/{}".format(directory, prefix)


def change_directory(path, current_directory):
    if path == "" or path == "~":
        current_directory = ""
    elif path.startswith("/"):
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


def get_relative_name(current_directory, filename):
    if filename.startswith(current_directory):
        relative_filename = _trim_leading_slash(filename[len(current_directory):])
        return relative_filename.split("/")[0]
    else:
        return None


def is_relative_file(current_directory, filename):
    if filename.startswith(current_directory):
        relative_filename = _trim_leading_slash(filename[len(current_directory):])
        if relative_filename and "/" not in relative_filename:
            return True
    return False


def is_relative_directory(current_directory, filename):
    if filename.startswith(current_directory):
        relative_filename = _trim_leading_slash(filename[len(current_directory):])
        if "/" in relative_filename:
            return True
    return False


def _trim_leading_slash(filename):
    if filename.startswith("/") and len(filename) > 1:
        return _trim_leading_slash(filename[1:])
    else:
        return filename
