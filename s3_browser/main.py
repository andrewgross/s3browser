# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from client import S3Browser


def main():

    while True:
        try:
            S3Browser(None, None).cmdloop()
        except KeyboardInterrupt:
            print("^C")  # noqa
            continue
        break


if __name__ == '__main__':
    main()
