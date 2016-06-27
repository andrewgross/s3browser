# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from client import S3Browser


def main():
    current_directory = ""

    while True:
        try:
            browser = S3Browser(None, None, current_directory=current_directory)
            browser.cmdloop()
        except KeyboardInterrupt:
            print("^C")  # noqa
            current_directory = browser.current_directory
            continue
        break


if __name__ == '__main__':
    main()
