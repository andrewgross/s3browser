# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from s3browser.list_utilities import (
    sort_files
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
