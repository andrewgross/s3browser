# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from freezegun import freeze_time

from s3browser.util.tree import S3File, S3Dir, add_key
from tests.util import S3File as BotoKey


def test_s3_file_get_size():
    """
    An S3File should return its size with get_size
    """
    # When I have an S3File
    f = S3File("foo", 42, datetime.datetime.now())

    # And I get the size
    size = f.get_size()

    # Then it returns the size
    size.should.equal(42)


def test_s3_file_get_last_modified():
    """
    An S3File should return its last modified time with get_last_modified
    """
    # When I have an S3File
    now = datetime.datetime.now()
    f = S3File("foo", 42, now)

    # And I get the last modified time
    lm = f.get_last_modified()

    # Then it returns the size
    lm.should.equal(now)


@freeze_time("2016-07-11 03:39:34")
def test_s3_file_get_last_modified_string():
    """
    An S3File populated with a string time should return its last modified time with get_last_modified
    """
    # When I have an S3File
    now_string = "2016-07-11T03:39:34.000Z"
    now = datetime.datetime.now()
    f = S3File("foo", 42, now_string)

    # And I get the last modified time
    lm = f.get_last_modified()

    # Then it returns the size
    lm.should.equal(now)


def test_s3_dir_size():
    """
    An S3Dir should accumulate the sizes of its children
    """
    # When I have S3 Files
    now = datetime.datetime.now()
    f1 = S3File("foo", 1, now)
    f2 = S3File("bar", 2, now)

    # And they are inside of a directory
    d = S3Dir("dir")
    d.add_child(f1)
    d.add_child(f2)

    # When I get the size
    size = d.get_size()

    # Then I get the accumulated size
    size.should.equal(3)


def test_s3_dir_size_nested():
    """
    An S3Dir should accumulate the sizes of its children including nested dirs
    """
    # When I have S3 Files
    now = datetime.datetime.now()
    f1 = S3File("foo", 1, now)
    f2 = S3File("bar", 4, now)

    # And they are inside of nested directories
    d2 = S3Dir("inner")
    d2.add_child(f2)

    d1 = S3Dir("outer")
    d1.add_child(d2)
    d1.add_child(f1)

    # When I get the size
    size_1 = d1.get_size()
    size_2 = d2.get_size()

    # Then I get the accumulated size
    size_1.should.equal(5)
    size_2.should.equal(4)


def test_s3_dir_bad_child():
    """
    An S3Dir should not let me add a bad child
    """
    # When I have an S3Dir
    d = S3Dir("foo")

    # If I try to add a non S3 object it should fail
    d.add_child.when.called_with("banana").should.throw(Exception)


def test_s3_dir_last_modified():
    """
    An S3Dir should show the latest last modified time of its children
    """
    # When I have an S3 Dir
    d1 = S3Dir("outer")
    d2 = S3Dir("inner")
    d1.add_child(d2)

    # And I have files
    new = datetime.datetime.now()
    old = datetime.datetime.now() - datetime.timedelta(hours=1)
    f1 = S3File("foo", 1, new)
    f2 = S3File("bar", 4, old)

    # And they are nested in directories
    d1.add_child(f1)
    d2.add_child(f2)

    # When I get the last modified time
    last_modified_1 = d1.get_last_modified()
    last_modified_2 = d2.get_last_modified()

    # Then it shows the lastest time of its children
    last_modified_1.should.equal(new)
    last_modified_2.should.equal(old)


def test_add_node():
    """
    add_node should add an S3File to a node if it is a file
    """
    # When I have a node
    node = S3Dir("")

    # And I have a boto key
    key = BotoKey("foo")

    # When I add the key to the node
    add_key(node, key, key.name)

    # Then It adds an S3File
    node.files[0].name.should.equal("foo")


def test_add_node_nested():
    """
    add_node should add nested nodes if given nested keys
    """
    # When I have a node
    node = S3Dir("")

    # And I have a boto key
    key = BotoKey("top/middle/foo")

    # When I add the key to the node
    add_key(node, key, key.name)

    # Then It adds the appropriate nodes
    node.dirs[0].name.should.equal("top")
    node.dirs[0].dirs[0].name.should.equal("middle")
    node.dirs[0].dirs[0].files[0].name.should.equal("foo")


def test_add_directory():
    """
    add_node should add directories without sub files
    """
    # When I have a node
    node = S3Dir("")

    # And I have a boto key
    key = BotoKey("top/aa/")
    key2 = BotoKey("top/zz")

    # When I add the key to the node
    add_key(node, key, key.name)
    add_key(node, key2, key2.name)

    # Then It adds the appropriate nodes
    node.dirs[0].name.should.equal("top")
    node.dirs[0].dirs[0].name.should.equal("aa")
    node.dirs[0].files[0].name.should.equal("zz")


def test_add_multiple_files_to_directory():
    """
    add_node should add directories with multiple sub files
    """
    # When I have a node
    node = S3Dir("")

    # And I have a boto key
    key = BotoKey("middle/aa")
    key2 = BotoKey("middle/zz")

    # When I add the key to the node
    add_key(node, key, key.name)
    add_key(node, key2, key2.name)

    # Then It adds the appropriate nodes
    node.dirs[0].name.should.equal("middle")
    node.dirs[0].files[0].name.should.equal("aa")
    node.dirs[0].files[1].name.should.equal("zz")


def test_add_directory_with_multiple_sub_directories():
    """
    add_node should add directories with multiple sub directories
    """
    # When I have a node
    node = S3Dir("")

    # And I have a boto key
    key = BotoKey("top/top/aa")
    key2 = BotoKey("top/bottom/zz")

    # When I add the key to the node
    add_key(node, key, key.name)
    add_key(node, key2, key2.name)

    # Then It adds the appropriate nodes
    node.dirs[0].name.should.equal("top")
    node.dirs[0].dirs[0].name.should.equal("top")
    node.dirs[0].dirs[1].name.should.equal("bottom")
    node.dirs[0].dirs[0].files[0].name.should.equal("aa")
    node.dirs[0].dirs[1].files[0].name.should.equal("zz")
