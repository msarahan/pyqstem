#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import qstem.about as about

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='pyqstem',
    version=about.__version__,
    description='Python Quantitative STEM simulation',
    long_description=readme + '\n\n' + history,
    author=about.__author__,
    author_email=about.__email__,
    url='https://github.com/msarahan/pyqstem',
    packages=[
        'pyqstem',
    ],
    package_dir={'pyqstem':
                 'pyqstem'},
    include_package_data=True,
    install_requires=[
    ],
    license="GPL v3",
    zip_safe=False,
    keywords='pyqstem',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)