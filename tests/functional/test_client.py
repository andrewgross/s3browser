# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from s3browser.client import S3Browser

from mock import patch
from moto import mock_s3
from tests.util import populate_bucket


@mock_s3
def test_refresh():
    """
    Refresh should get all keys in a bucket
    """
    # When I have a bucket with keys
    keys = ['foo', 'bar']
    bucket, conn = populate_bucket('mybucket', keys)

    # And I have a client
    c = S3Browser(bucket, conn)

    # When I refresh
    c.do_refresh("")

    # Then I get all of my keys
    set(map(lambda x: x.name, c.keys)).should.equal(set(keys))


@mock_s3
@patch('s3browser.client.print_result')
def test_pwd(output):
    """
    pwd should show the current directory
    """
    # When I have a client
    keys = ['foo', 'bar']
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(bucket, conn)

    # And I have a current directory
    current_directory = "foo/bar/baz"
    c.current_directory = current_directory

    # When I call pwd
    c.do_pwd("")

    # Then I get the current directory
    output.assert_called_once_with(current_directory)
