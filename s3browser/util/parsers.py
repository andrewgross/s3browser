# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from argparse import ArgumentParser


def main_parser():
    parser = ArgumentParser(prog="s3browser", description="Run S3Browser")

    parser.add_argument(
        "--access-key-id",
        dest="access_key_id",
        type=str,
        default=None,
        help='AWS_ACCESS_KEY_ID used by Boto',
        action="store",
        required=False
    )

    parser.add_argument(
        "--secret-access-key",
        dest="secret_access_key",
        type=str,
        default=None,
        help='AWS_SECRET_ACCESS_KEY used by Boto',
        action="store",
        required=False
    )
    return parser


def ls_parser():
    parser = ArgumentParser(prog="ls", description="List Files", add_help=False)

    parser.add_argument(
        "expression",
        metavar="<expression>",
        nargs='?',
        type=str,
        help='Regex filtering expression',
        action="store",
    )

    parser.add_argument(
        "-l",
        dest="long",
        default=False,
        help='List in Long Format',
        action="store_true",
        required=False
    )

    parser.add_argument(
        "-h",
        dest="human",
        default=False,
        help='Display sizes as human readable',
        action="store_true",
        required=False
    )

    parser.add_argument(
        "-r",
        dest="reverse",
        default=False,
        help='Reverse sort order',
        action="store_true",
        required=False
    )

    sorting = parser.add_mutually_exclusive_group()

    sorting.add_argument(
        "-S",
        dest="size",
        default=False,
        help='Sort by File Size',
        action="store_true",
        required=False
    )

    sorting.add_argument(
        "-t",
        dest="time",
        default=False,
        help='Sort by last_modified',
        action="store_true",
        required=False
    )

    return parser
