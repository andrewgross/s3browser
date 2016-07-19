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
    c = S3Browser(conn)

    # When I refresh
    with silence_stdout():
        c.do_refresh("mybucket")

    # Then I get all of my keys
    len(c.current_directory.files).should.equal(2)


@mock_s3
@patch('s3browser.client.print_result')
def test_pwd(output):
    """
    pwd should show the current directory
    """
    # When I have a client
    keys = ["foo", "bar"]
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(conn)

    # And I have files
    with silence_stdout():
        c.do_refresh("mybucket")

    # When I call pwd
    c.do_pwd("")

    # Then I get the top level bucket name
    output.assert_called_once_with("/mybucket")


@mock_s3
@patch('s3browser.util.list.print_result')
def test_ls(output):
    """
    ls should show the current files
    """
    # When I have a client
    keys = ["foo", "bar"]
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("mybucket")

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
    c = S3Browser(conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("mybucket")

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
    c = S3Browser(conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("mybucket")

    # When I call ls
    c.do_ls("-l")

    # Then I get the current files and directories
    expected = [call("              3B", "2016-07-11 03:39", "bar"), call("              3B", "2016-07-11 03:39", "foo")]
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
    c = S3Browser(conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("mybucket")

    # When I call ls
    c.do_ls("-lh")

    # Then I get the current files and directories
    expected = [call("   3B", "2016-07-11 03:39", "bar"), call("   3B", "2016-07-11 03:39", "foo")]
    assert output.call_args_list == expected


@mock_s3
@freeze_time("2016-07-11 03:39:34")
@patch('s3browser.util.list.print_result')
def test_ls_lhsr(output):
    """
    ls -lhsr should sort by size, reversed
    """
    # When I have a client
    keys = ["fooz", "bar"]
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("mybucket")

    # When I call ls
    c.do_ls("-lhSr")

    # Then I get the current files and directories
    expected = [
        call("   4B", "2016-07-11 03:39", "fooz"),
        call("   3B", "2016-07-11 03:39", "bar"),
    ]
    assert output.call_args_list == expected


@mock_s3
@patch('s3browser.util.list.print_result')
def test_ls_lht(output):
    """
    ls -lht should sort by last modified, reversed
    """
    # When I have a client
    with freeze_time("2016-07-11 03:39:34"):
        keys = ["new"]
        bucket, conn = populate_bucket('mybucket', keys)
    with freeze_time("2016-07-10 03:39:34"):
        keys = ["old"]
        bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("mybucket")

    # When I call ls
    c.do_ls("-lht")

    # Then I get the current files and directories
    expected = [
        call("   3B", "2016-07-11 03:39", "new"),
        call("   3B", "2016-07-10 03:39", "old"),
    ]
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
    c = S3Browser(conn)

    # And I have no current directory
    current_directory = ""
    c.current_directory = current_directory
    with silence_stdout():
        c.do_refresh("mybucket")

    # When I call ls
    c.do_ls("-l")

    # Then I get the current files and directories
    expected = [
        call("             14B", "2016-07-11 03:39", color_blue("foo")),
        call("              4B", "2016-07-11 03:39", "foo2")
    ]
    assert output.call_args_list == expected


@mock_s3
@freeze_time("2016-07-11 03:39:34")
@patch('s3browser.util.list.print_result')
def test_ls_nested(output):
    """
    ls should work with a current directory.
    """
    # When I have a client
    keys = ["foo/foo/bar/baz", "foo/bar2", "foo/baz2/baz3", "banana"]
    bucket, conn = populate_bucket('mybucket', keys)
    c = S3Browser(conn)
    with silence_stdout():
        c.do_refresh("mybucket")

    # And I have a current directory
    c.do_cd("foo")

    # When I call ls
    c.do_ls("")

    # Then I get the current files and directories
    expected = [call("bar2"), call(color_blue("baz2")), call(color_blue("foo"))]
    assert output.call_args_list == expected
