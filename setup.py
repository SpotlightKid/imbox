#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup

version = '0.6'


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='imbox',
    version=version,
    description="Python IMAP for Human beings",
    long_description=read('README.md'),
    keywords='email, IMAP, parsing emails',
    author='Martin Rusev',
    author_email='martinrusev@live.com',
    maintainer='Christopher Arndt',
    maintainer_email='chris@chrisarndt.de',
    url='https://github.com/spotlightkid/imbox',
    license='MIT',
    packages=['imbox'],
    package_dir={'imbox': 'imbox'},
    install_requires=['imapclient'],
    tests_require=['nose>=1.0', 'tox'],
    test_suite='nose.collector',
    zip_safe=False
)
