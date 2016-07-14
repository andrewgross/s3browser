# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def get_pwd(node):
    if not node.parent:
        return node.name
    return "{}/{}".format(get_pwd(node.parent), node.name)


def get_root_node(node):
    if node.parent:
        return get_root_node(node.parent)
    return node


def change_directory(path, current_node):
    if path in ["", "~", "/"]:
        return get_root_node(current_node)
    if path.startswith("/"):
        path = path[1:]
        current_node = get_root_node(current_node)
    for p in path.split("/"):
        if p == ".":
            continue
        elif p == "..":
            if current_node.parent:
                current_node = current_node.parent
        else:
            child = _get_matching_dir(p, current_node)
            if child is None:
                return None
            current_node = child
    return current_node


def _get_matching_dir(name, node):
    for child in node.dirs:
        if child.name == name:
            return child
