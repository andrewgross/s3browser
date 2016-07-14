# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from s3browser.util.path import (
    change_directory,
    get_pwd,
)

from s3browser.util.tree import S3Dir


def test_change_directory_no_base_no_path():
    """
    Change Directory with no current directory and no path
    """
    # When I have no directory
    current_directory = S3Dir("")

    # And I have no path
    path = ""

    # Then I stay with no directory
    change_directory(path, current_directory).name.should.equal("")


def test_change_directory_with_base_no_path():
    """
    Change Directory with a current directory and no path
    """
    # When I have a directory
    current_directory = S3Dir("foo")
    top_level = S3Dir("")
    top_level.add_child(current_directory)

    # And I have no path
    path = ""

    # Then I go back to the top level
    change_directory(path, current_directory).name.should.equal("")


def test_change_directory_with_tilde():
    """
    Change Directory with a current directory and tilde
    """
    # When I have a directory
    current_directory = S3Dir("foo")
    top_level = S3Dir("")
    top_level.add_child(current_directory)

    # And I have a tilde for a path
    path = "~"

    # Then I go back to the top level
    change_directory(path, current_directory).name.should.equal("")


def test_change_directory_with_leading_slash_in_path():
    """
    Change Directory with a current directory and a leading slash in the path
    """
    # When I have a directory
    current_directory = S3Dir("foo")
    top = S3Dir("")
    middle = S3Dir("bar")
    top.add_child(current_directory)
    top.add_child(middle)

    # And I have a leading / path
    path = "/bar"

    # Then I go to a top level directory
    change_directory(path, current_directory).name.should.equal("bar")


def test_change_directory_with_base_and_path():
    """
    Change Directory with a directory and a path
    """
    # When I have a directory
    current_directory = S3Dir("foo")
    top = S3Dir("")
    bottom = S3Dir("bar")
    top.add_child(current_directory)
    current_directory.add_child(bottom)

    # And I have a path
    path = "bar"

    # Then I stay build a new path
    _current = change_directory(path, current_directory)
    _current.name.should.equal("bar")
    get_pwd(_current).should.equal("/foo/bar")


def test_change_directory_with_compound_base():
    """
    Change Directory with a compound directory and a path
    """
    # When I have a deep directory structure
    current_directory = S3Dir("baz")
    top = S3Dir("")
    middle = S3Dir("foo")
    bottom = S3Dir("bar")
    top.add_child(middle)
    middle.add_child(current_directory)
    current_directory.add_child(bottom)

    # And I have a path
    path = "bar"

    # Then I build a new path
    _current = change_directory(path, current_directory)
    _current.name.should.equal("bar")
    get_pwd(_current).should.equal("/foo/baz/bar")


def test_change_directory_with_compound_path():
    """
    Change Directory with a directory and a compound path
    """
    # When I have a directory
    current_directory = "foo"
    current_directory = S3Dir("foo")
    top = S3Dir("")
    middle = S3Dir("baz")
    bottom = S3Dir("bar")
    top.add_child(current_directory)
    current_directory.add_child(middle)
    middle.add_child(bottom)

    # And I have a nested path
    path = "baz/bar"

    # Then I build a new path
    _current = change_directory(path, current_directory)
    _current.name.should.equal("bar")
    get_pwd(_current).should.equal("/foo/baz/bar")


def test_change_directory_with_single_dot_path():
    """
    Change Directory with a directory and a path with a single dot
    """
    # When I have a directory
    current_directory = S3Dir("foo")
    top = S3Dir("")
    top.add_child(current_directory)

    # And I have a path
    path = "."

    # Then I stay in my current directory
    change_directory(path, current_directory).name.should.equal("foo")


def test_change_directory_with_double_dot_path():
    """
    Change Directory with a directory and a path with a double dot
    """
    # When I have a directory tree
    top = S3Dir("")
    middle = S3Dir("foo")
    bottom = S3Dir("bar")
    top.add_child(middle)
    middle.add_child(bottom)

    # And I have a current directory
    current_directory = bottom

    # And I have a path
    path = ".."

    # Then I move up one level
    change_directory(path, current_directory).name.should.equal("foo")


def test_change_directory_with_path_with_single_dot_in_it():
    """
    Change Directory with a directory and a compound path with a single dot
    """
    # When I have a directory structure
    top = S3Dir("")
    foo = S3Dir("foo")
    bar = S3Dir("bar")
    baz = S3Dir("baz")
    bat = S3Dir("bat")

    top.add_child(foo)
    foo.add_child(bar)
    bar.add_child(baz)
    baz.add_child(bat)

    # And I have a current directory
    current_directory = bar

    # And I have a path
    path = "baz/./bat"

    # Then I stay in my current directory
    _current = change_directory(path, current_directory)
    _current.name.should.equal("bat")
    get_pwd(_current).should.equal("/foo/bar/baz/bat")


def test_change_directory_with_path_with_double_dot_in_it():
    """
    Change Directory with a directory and a compound path with a double dot
    """
    # When I have a directory structure
    top = S3Dir("")
    foo = S3Dir("foo")
    bar = S3Dir("bar")
    bat = S3Dir("bat")
    baz = S3Dir("baz")

    top.add_child(foo)
    foo.add_child(bar)
    bar.add_child(bat)
    bar.add_child(baz)

    # And I have a current directory
    current_directory = bar

    # And I have a path
    path = "baz/../bat"

    # Then I navigate to the correct directory
    _current = change_directory(path, current_directory)
    _current.name.should.equal("bat")
    get_pwd(_current).should.equal("/foo/bar/bat")


def test_change_directory_go_up_from_top():
    """
    Change Directory with double dot from top level
    """
    # When I have a directory structure
    top = S3Dir("")

    # And I have a current directory
    current_directory = top

    # And I have a path
    path = ".."

    # Then I navigate to the correct directory
    _current = change_directory(path, current_directory)
    _current.name.should.equal("")
    get_pwd(_current).should.equal("")


def test_change_directory_to_nonexistent_dir():
    """
    Change Directory to a non existent directory
    """
    # When I have a directory structure
    top = S3Dir("top")
    middle = S3Dir("middle")
    bottom = S3Dir("bottom")

    top.add_child(middle)
    middle.add_child(bottom)

    # And I have a current directory
    current_directory = middle

    # And I have an invalid path
    path = "foo"

    # Then I do not go into that directory
    change_directory(path, current_directory).should.be.none
