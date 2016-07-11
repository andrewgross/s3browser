# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from client import S3Browser
from .util.s3 import get_connection, get_bucket
from .util.parsers import main_parser
from . import __version__


def main():
    parser = main_parser()
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
