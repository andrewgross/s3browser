#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import os
from setuptools import setup, find_packages

version = ''
with open('s3browser/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


def parse_requirements():
    """Rudimentary parser for the `requirements.txt` file
    We just want to separate regular packages from links to pass them to the
    `install_requires` and `dependency_links` params of the `setup()`
    function properly.
    """
    try:
        requirements = \
            map(str.strip, local_file('requirements.txt').splitlines())
    except IOError:
        raise RuntimeError("Couldn't find the `requirements.txt' file :(")

    links = []
    pkgs = []
    for req in requirements:
        if not req:
            continue
        if 'http:' in req or 'https:' in req:
            links.append(req)
            name, version = re.findall("\#egg=([^\-]+)-(.+$)", req)[0]
            pkgs.append('{0}=={1}'.format(name, version))
        else:
            pkgs.append(req)

    return pkgs, links


def local_file(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read()

install_requires, dependency_links = parse_requirements()

if __name__ == '__main__':

    setup(
        name="s3browser",
        version=version,
        description="s3browser",
        long_description=local_file('README.md'),
        author='Andrew Gross',
        author_email='andrew.w.gross@gmail.com',
        url='https://github.com/andrewgross/s3browser',
        packages=find_packages(exclude=['*tests*']),
        install_requires=install_requires,
        include_package_data=True,
        dependency_links=dependency_links,
        classifiers=[
            'Programming Language :: Python',
        ],
        zip_safe=False,
        entry_points={
            'console_scripts': [
                's3browser = s3browser.main:main'
            ],
        },
    )
