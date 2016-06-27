# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from s3browser.list_utilities import (
    sort_files,
    get_names,
    get_matches
)
from tests.util import get_unsorted_list_of_files


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
