#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

__version__ = '0.0.1'

setup(
    name='flickr_caller',
    version=__version__,
    long_description=long_description,
    description='Wrapper around Flickr API client.',
    url='https://github.com/rfaulkner/flickr-caller',
    author="Ryan Faulkner",
    author_email="rfaulk@yahoo-inc.com",
    packages=['flickr_caller',],
    install_requires=[
        'flickrapi >= 1.4.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    data_files=[('readme', ['README.md'])]
)
