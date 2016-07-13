# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from freezegun import freeze_time

from s3browser.util.list import (
    sort_files,
    get_names,
    get_matches,
    get_sub_directory_names,
    get_sub_file_names,
    _get_date,
    _get_size,
)
from tests.util import get_unsorted_list_of_files, S3File


def test_sort_files():
    """
    Sort files based on key name
    """
    # When I have an unsorted list of files
    files = get_unsorted_list_of_files()

    # And I sort them with the defaults
    _sorted = sort_files(files)

    # Then I have sorted files
    map(lambda x: x.name, _sorted).should.equal(["a", "b", "c"])


def test_get_names():
    """
    Get names from file objects
    """
    # When I have an unsorted list of files
    files = get_unsorted_list_of_files()

    # And when I get the names
    names = get_names(files)

    # Then I have just names
    set(names).should.equal(set(("a", "b", "c")))


def test_get_matches():
    """
    Filter files to a list of matches
    """
    # When I have a list of files
    files = get_unsorted_list_of_files()

    # And when I get the matches
    matches = get_matches("a", files)

    # Then I have just that match
    map(lambda x: x.name, matches).should.equal(["a"])


def test_get_directories():
    """
    Filter a list of files to directories in the current directory.
    """
    # When I have a file of nested directories
    a = S3File("foo/bar/a")
    b = S3File("foo/b")
    c = S3File("c")
    files = [a, b, c]

    # And I have a current directory
    current_directory = "foo"

    # When I get sub directories of my current directory
    result = get_sub_directory_names(current_directory, files)

    # Then I only get the sub directories
    result.should.equal(["bar"])


def test_get_directories_with_trailing_slash():
    """
    Filter a list of files to directories in the current directory.
    """
    # When I have a file of nested directories
    a = S3File("foo/bar/a")
    b = S3File("foo/b")
    c = S3File("c")
    files = [a, b, c]

    # And I have a current directory
    current_directory = "foo/"

    # When I get sub directories of my current directory
    result = get_sub_directory_names(current_directory, files)

    # Then I only get the sub directories
    result.should.equal(["bar"])


def test_get_filenames():
    """
    Filter a list of files to filenames in the current directory.
    """
    # When I have a file of nested directories
    a = S3File("foo/bar/a")
    b = S3File("foo/b")
    c = S3File("c")
    files = [a, b, c]

    # And I have a current directory
    current_directory = "foo"

    # When I get sub files of my current directory
    result = get_sub_file_names(current_directory, files)

    # Then I only get the sub files
    result.should.equal(["b"])


def test_get_files_with_trailing_slash():
    """
    Filter a list of files to files does not include trailing slashes.
    """
    # When I have a file of nested directories
    a = S3File("foo/d/")
    b = S3File("foo/b")
    files = [a, b]

    # And I have a current directory
    current_directory = "foo"

    # When I get sub files of my current directory
    result = get_sub_file_names(current_directory, files)

    # Then I only get the sub files not directories
    result.should.equal(["b"])


def test_get_files_with_empty_string():
    """
    Filter a list of files to files does not include the directory name.
    """
    # When I have files with a directory and sub files
    a = S3File("foo/")
    b = S3File("foo/b")
    files = [a, b]

    # And I have a current directory
    current_directory = "foo"

    # When I get sub files of my current directory
    result = get_sub_file_names(current_directory, files)

    # Then I only get the sub files not directories
    result.should.equal(["b"])


def test_get_files_with_matching_subdirectories():
    """
    Filter a list of files to files works with filenames.
    """
    # When I have files with a directory and sub files
    a = S3File("foo/b/")
    b = S3File("foo/bo")
    files = [a, b]

    # And I have a current directory
    current_directory = "foo/"

    # When I get sub files of my current directory
    result = get_sub_file_names(current_directory, files)

    # Then I only get the sub files not directories
    result.should.equal(["bo"])


@freeze_time("2016-07-11 03:39:34")
def test_get_last_modified():
    """
    Given a filename, get the latest modification timestamp for all sub files
    """
    # When I have a filename
    filename = "foo"

    # And I have a set of files
    def _format(date):
        return date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    old = datetime.datetime.now() - datetime.timedelta(hours=1)
    new = datetime.datetime.now()
    old_file = S3File("foo/old", last_modified=_format(old))
    new_file = S3File("foo/new", last_modified=_format(new))
    collapsed_files = {
        "foo": [old_file, new_file]
    }

    # When I get the latest modified date
    last_modified = _get_date(filename, collapsed_files)

    # Then I get the new date
    last_modified.should.equal(new)


def test_get_size():
    """
    Given a filename, get the total size for all sub files
    """
    # When I have a filename
    filename = "foo"

    # And I have a set of files
    old_file = S3File("foo/old", size=1)
    new_file = S3File("foo/new", size=2)
    collapsed_files = {
        "foo": [old_file, new_file]
    }

    # When I get the size
    size = _get_size(filename, collapsed_files)

    # Then I get the total size
    size.should.equal(3)
