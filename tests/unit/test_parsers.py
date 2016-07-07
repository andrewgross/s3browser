# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from s3browser.list_utilities import parse_ls
from s3browser.parsers import main_parser
from s3browser.decorators import silence_stderr


def test_parse_ls():
    """
    Test parsing ls command with empty args
    """
    # When I have an ls command
    command = ""

    # And I parse it
    parsed = parse_ls(command)

    # Then I get a parsed command with defaults
    parsed.reverse.should.be.false
    parsed.size.should.be.false
    parsed.human.should.be.false
    parsed.time.should.be.false
    parsed.long.should.be.false


def test_parse_ls_l():
    """
    Test parsing ls command with long
    """
    # When I have an ls command
    command = "-l"

    # And I parse it
    parsed = parse_ls(command)

    # Then I get a parsed command with long set
    parsed.reverse.should.be.false
    parsed.size.should.be.false
    parsed.human.should.be.false
    parsed.time.should.be.false
    parsed.long.should.be.true


def test_parse_ls_s():
    """
    Test parsing ls command with size
    """
    # When I have an ls command
    command = "-s"

    # And I parse it
    parsed = parse_ls(command)

    # Then I get a parsed command with size set
    parsed.reverse.should.be.false
    parsed.size.should.be.true
    parsed.human.should.be.false
    parsed.time.should.be.false
    parsed.long.should.be.false


def test_parse_ls_t():
    """
    Test parsing ls command with time
    """
    # When I have an ls command
    command = "-t"

    # And I parse it
    parsed = parse_ls(command)

    # Then I get a parsed command with time set
    parsed.reverse.should.be.false
    parsed.size.should.be.false
    parsed.human.should.be.false
    parsed.time.should.be.true
    parsed.long.should.be.false


def test_parse_ls_r():
    """
    Test parsing ls command with reverse
    """
    # When I have an ls command
    command = "-r"

    # And I parse it
    parsed = parse_ls(command)

    # Then I get a parsed command with reverse set
    parsed.reverse.should.be.true
    parsed.size.should.be.false
    parsed.human.should.be.false
    parsed.time.should.be.false
    parsed.long.should.be.false


def test_parse_ls_h():
    """
    Test parsing ls command with human
    """
    # When I have an ls command
    command = "-h"

    # And I parse it
    parsed = parse_ls(command)

    # Then I get a parsed command with human set
    parsed.reverse.should.be.false
    parsed.size.should.be.false
    parsed.human.should.be.true
    parsed.time.should.be.false
    parsed.long.should.be.false


def test_parse_ls_multiple():
    """
    Test parsing ls command with multiple flags
    """
    # When I have an ls command
    command = "-lhtr"

    # And I parse it
    parsed = parse_ls(command)

    # Then I get a parsed command with multiple flags set
    parsed.reverse.should.be.true
    parsed.size.should.be.false
    parsed.human.should.be.true
    parsed.time.should.be.true
    parsed.long.should.be.true


def test_parse_ls_exclusive():
    """
    Test parsing ls command with mutually exclusive flags
    """
    # When I have an ls command with exclusive flags
    command = "-ts"

    # And I parse it
    with silence_stderr():
        parsed = parse_ls(command)

    # Then I get back nothing
    parsed.should.be.none


def test_parse_ls_expression():
    """
    Test parsing ls command with expression
    """
    # When I have an ls command
    command = "*foobar*"

    # And I parse it
    parsed = parse_ls(command)

    # Then I get a parsed command with no flags but an expression
    parsed.reverse.should.be.false
    parsed.size.should.be.false
    parsed.human.should.be.false
    parsed.time.should.be.false
    parsed.long.should.be.false
    parsed.expression.should.equal(command)


def test_parse_ls_bad_args():
    """
    Test parsing ls command with bad_arguments
    """
    # When I have an bad ls command
    command = "-laGh"

    # And I parse it
    with silence_stderr():
        parsed = parse_ls(command)

    # Then I get back nothing
    parsed.should.be.none


def test_main_parser():
    """
    Test main parser
    """
    # When I have a parser
    parser = main_parser()

    # And I have a command
    command = "my_bucket --access-key-id foo --secret-access-key bar"

    # And I parse it
    parsed = parser.parse_args(command.split(" "))

    # Then I get my arguments
    parsed.bucket = "my_bucket"
    parsed.access_key_id = "foo"
    parsed.secret_access_key = "bar"
