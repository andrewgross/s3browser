# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from s3browser.util.path import (
    change_directory,
    get_path,
    get_relative_name,
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


def test_get_relative_name():
    """
    Get Relative Filenames with no current directory and a file
    """
    # When I have a file
    filename = "foo.txt"

    # And I have no current directory
    current_directory = ""

    # Then I get the filename
    get_relative_name(current_directory, filename).should.equal("foo.txt")


def test_get_relative_name_with_nested_name():
    """
    Get Relative Filename with a current directory and nested files
    """
    # When I have a file with nested structure
    filename = "top_level/foo.txt"

    # And I have a current directory
    current_directory = "top_level"

    # Then I get the relative filename
    get_relative_name(current_directory, filename).should.equal("foo.txt")


def test_get_relative_name_with_nested_directory_name():
    """
    Get Relative Filename with a current directory and nested directories
    """
    # When I have a file with nested structure
    filename = "top_level/middle_level/foo.txt"

    # And I have a current directory
    current_directory = "top_level"

    # Then I get the relative directory name
    get_relative_name(current_directory, filename).should.equal("middle_level")


def test_get_relative_name_with_deeply_nested_file_name():
    """
    Get Relative Filename with a current directory and deeply nested filename
    """
    # When I have a file with nested structure
    filename = "top_level/middle_level/foo.txt"

    # And I have a nested current directory
    current_directory = "top_level/middle_level"

    # Then I get the relative filename
    get_relative_name(current_directory, filename).should.equal("foo.txt")


def test_get_relative_name_with_adjacent_slashes_in_filename():
    """
    Get Relative Filename with a current directory and a filename with adjacent slashes
    """
    # When I have a file with nested structure
    filename = "top_level/middle_level//foo.txt"

    # And I have a nested current directory
    current_directory = "top_level/middle_level"

    # Then I get the relative filename
    get_relative_name(current_directory, filename).should.equal("foo.txt")


def test_get_relative_name_with_mismatched_directory():
    """
    Get Relative Filename with a current directory that does not match filename
    """
    # When I have a file with nested structure
    filename = "top_level/foo.txt"

    # And I have a current directory that does not match
    current_directory = "something_bad"

    # Then I get back None
    get_relative_name(current_directory, filename).should.equal(None)
