# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Python setup.py installer script."""

# Standard library imports
import ast
import os
import sys

# Third party imports
from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='pyswmm'):
    """Get version."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()
    lines = data.split('\n')
    for line in lines:
        if line.startswith('VERSION_INFO'):
            version_tuple = ast.literal_eval(line.split('=')[-1].strip())
            version = '.'.join(map(str, version_tuple))
            break
    return version


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.md'), 'r') as f:
        data = f.read()
    return data


REQUIREMENTS = ['swmm-toolkit>=0.9.0',
                'julian>=0.14',
                'aenum>=3.1.11']


setup(
    name='pyswmm',
    version=get_version(),
    description='Python Wrapper for SWMM5 API',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/OpenWaterAnalytics/pyswmm/wiki',
    author='Bryant E. McDonnell (See AUTHORS)',
    install_requires=REQUIREMENTS,
    extras_require = {
        '5.1.14':['swmm-toolkit==0.9.1'],
        '5.1.15':['swmm-toolkit==0.10.0'],
        '5.2.0' :['swmm-toolkit==0.11.0'],
        '5.2.1' :['swmm-toolkit==0.12.0'],
        '5.2.2' :['swmm-toolkit==0.13.0'],
        '5.2.3' :['swmm-toolkit==0.14.0'],
    },
    packages=find_packages(exclude=['contrib', 'docs']),
    package_data={
        '': ['LICENSE.txt', 'AUTHORS', 'tests/data/*.inp', 'tests/*.py']
    },
    include_package_data=True,
    license="BSD2 License",
    keywords="swmm5, swmm, hydraulics, hydrology, modeling, collection system",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Documentation :: Sphinx",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
    ])
