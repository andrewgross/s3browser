# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from argparse import ArgumentParser

from client import S3Browser
from .s3_utilities import get_connection, get_bucket
from . import __version__


def main():
    parser = ArgumentParser(prog="s3browser", description="Run S3Browser for the given bucket")

    parser.add_argument(
        "bucket",
        metavar="BUCKET",
        type=str,
        help='Queues to process',
        action="store",
    )

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

    args = parser.parse_args()

    _main(args.bucket,
          access_key_id=args.access_key_id,
          secret_access_key=args.secret_access_key
          )


def _main(bucket_name, access_key_id=None, secret_access_key=None):
    print("Starting s3browser version {}".format(__version__))
    browser = None
    connection = get_connection(access_key_id=access_key_id, secret_access_key=secret_access_key)
    bucket = get_bucket(bucket_name, connection)

    while True:
        try:
            if not browser:
                browser = S3Browser(bucket, connection)
            browser.cmdloop()
        except KeyboardInterrupt:
            print("^C")  # noqa
            continue
        break


if __name__ == '__main__':
    main()
