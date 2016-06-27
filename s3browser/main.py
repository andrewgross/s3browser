# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from client import S3Browser


def main():
    browser = None

    while True:
        try:
            if not browser:
                browser = S3Browser(None, None)
            browser.cmdloop()
        except KeyboardInterrupt:
            print("^C")  # noqa
            continue
        break


if __name__ == '__main__':
    main()
