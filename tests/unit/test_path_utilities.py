# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from s3browser.path_utilities import (
    change_directory,
    get_path,
)


def test_get_path_no_prefix():
    """
    Build a path with no prefix
    """
    # When I have a directory
    directory = "foo/bar"

    # And I dont have a prefix
    prefix = None

    # Then I don't merge the empty prefix
    get_path(directory, prefix=prefix).should.equal(directory)


def test_get_path_no_directory():
    """
    Build a path with no directory
    """
    # When I have no directory
    directory = ""

    # And I have a prefix
    prefix = "foo"

    # Then I don't merge the empty directory
    get_path(directory, prefix=prefix).should.equal(prefix)


def test_get_path_with_prefix():
    """
    Build a path with with a prefix
    """
    # When I have a directory
    directory = "foo/bar"

    # And I have a prefix
    prefix = "baz"

    # Then I merge the empty prefix
    get_path(directory, prefix=prefix).should.equal("foo/bar/baz")


def test_change_directory_no_base_no_path():
    """
    Change Directory with no current directory and no path
    """
    # When I have no directory
    current_directory = ""

    # And I have no path
    path = ""

    # Then I stay with no directory
    change_directory(path, current_directory).should.equal("")


def test_change_directory_with_base_no_path():
    """
    Change Directory with a current directory and no path
    """
    # When I have a directory
    current_directory = "foo"

    # And I have no path
    path = ""

    # Then I go back to the top level
    change_directory(path, current_directory).should.equal("")


def test_change_directory_with_tilde():
    """
    Change Directory with a current directory and tilde
    """
    # When I have a directory
    current_directory = "foo"

    # And I have a tilde for a path
    path = "~"

    # Then I go back to the top level
    change_directory(path, current_directory).should.equal("")


def test_change_directory_with_leading_slash_in_path():
    """
    Change Directory with a current directory and a leading slash in the path
    """
    # When I have a directory
    current_directory = "foo"

    # And I have no path
    path = "/bar"

    # Then I stay with a directory
    change_directory(path, current_directory).should.equal("bar")


def test_change_directory_with_base_and_path():
    """
    Change Directory with a directory and a path
    """
    # When I have a directory
    current_directory = "foo"

    # And I have a path
    path = "bar"

    # Then I stay build a new path
    change_directory(path, current_directory).should.equal("foo/bar")


def test_change_directory_with_compound_base():
    """
    Change Directory with a compound directory and a path
    """
    # When I have a directory
    current_directory = "foo/baz"

    # And I have a path
    path = "bar"

    # Then I stay build a new path
    change_directory(path, current_directory).should.equal("foo/baz/bar")


def test_change_directory_with_compound_path():
    """
    Change Directory with a directory and a compound path
    """
    # When I have a directory
    current_directory = "foo"

    # And I have a path
    path = "baz/bar"

    # Then I stay build a new path
    change_directory(path, current_directory).should.equal("foo/baz/bar")


def test_change_directory_with_single_dot_path():
    """
    Change Directory with a directory and a path with a single dot
    """
    # When I have a directory
    current_directory = "foo"

    # And I have a path
    path = "."

    # Then I stay in my current directory
    change_directory(path, current_directory).should.equal("foo")


def test_change_directory_with_double_dot_path():
    """
    Change Directory with a directory and a path with a double dot
    """
    # When I have a directory
    current_directory = "foo/bar"

    # And I have a path
    path = ".."

    # Then I move up one level
    change_directory(path, current_directory).should.equal("foo")


def test_change_directory_with_path_with_single_dot_in_it():
    """
    Change Directory with a directory and a compound path with a single dot
    """
    # When I have a directory
    current_directory = "foo/bar"

    # And I have a path
    path = "baz/./bat"

    # Then I stay in my current directory
    change_directory(path, current_directory).should.equal("foo/bar/baz/bat")


def test_change_directory_with_path_with_double_dot_in_it():
    """
    Change Directory with a directory and a compound path with a double dot
    """
    # When I have a directory
    current_directory = "foo/bar"

    # And I have a path
    path = "baz/../bat"

    # Then I stay in my current directory
    change_directory(path, current_directory).should.equal("foo/bar/bat")
