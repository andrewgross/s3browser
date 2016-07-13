# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from s3browser.client import S3Browser
from s3browser.helpers import color_blue
from s3browser.util.decorators import silence_stdout

from freezegun import freeze_time
from mock import patch, call
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
    with silence_stdout():
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
    keys = []
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(bucket, conn)

    # And I have a current directory
    current_directory = "foo/bar/baz"
    c.current_directory = current_directory

    # When I call pwd
    c.do_pwd("")

    # Then I get the current directory
    output.assert_called_once_with(current_directory)


@mock_s3
@patch('s3browser.util.list.print_result')
def test_ls(output):
    """
    ls should show the current files
    """
    # When I have a client
    keys = ["foo", "bar"]
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(bucket, conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("")

    # When I call ls
    c.do_ls("")

    # Then I get the current files
    expected = [call("bar"), call("foo")]
    assert output.call_args_list == expected


@mock_s3
@patch('s3browser.util.list.print_result')
def test_ls_directory(output):
    """
    ls should show directories
    """
    # When I have a client
    keys = ["baz", "foo/bar"]
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(bucket, conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("")

    # When I call ls
    c.do_ls("")

    # Then I get the current files and directories
    expected = [call("baz"), call(color_blue("foo"))]
    assert output.call_args_list == expected


@mock_s3
@freeze_time("2016-07-11 03:39:34")
@patch('s3browser.util.list.print_result')
def test_ls_l(output):
    """
    ls -l should show size and last modified time
    """
    # When I have a client
    keys = ["foo", "bar"]
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(bucket, conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("")

    # When I call ls
    c.do_ls("-l")

    # Then I get the current files and directories
    expected = [call(3, "2016-07-11 03:39", "bar"), call(3, "2016-07-11 03:39", "foo")]
    assert output.call_args_list == expected


@mock_s3
@freeze_time("2016-07-11 03:39:34")
@patch('s3browser.util.list.print_result')
def test_ls_lh(output):
    """
    ls -lh should show human readable size
    """
    # When I have a client
    keys = ["foo", "bar"]
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(bucket, conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("")

    # When I call ls
    c.do_ls("-lh")

    # Then I get the current files and directories
    expected = [call("   3B", "2016-07-11 03:39", "bar"), call("   3B", "2016-07-11 03:39", "foo")]
    assert output.call_args_list == expected


@mock_s3
@freeze_time("2016-07-11 03:39:34")
@patch('s3browser.util.list.print_result')
def test_ls_l_size(output):
    """
    ls -l should sum directory contents sizes and not duplicate entries
    """
    # When I have a client
    keys = ["foo/bar", "foo/baz", "foo2"]
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(bucket, conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("")

    # When I call ls
    c.do_ls("-l")

    # Then I get the current files and directories
    expected = [call(14, "2016-07-11 03:39", color_blue("foo")), call(4, "2016-07-11 03:39", "foo2")]
    assert output.call_args_list == expected
