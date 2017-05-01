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
PY2 = sys.version_info.major == 2


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
    with open(os.path.join(HERE, 'README.rst'), 'r') as f:
        data = f.read()
    return data


REQUIREMENTS = ['six']

if sys.version_info < (3, 4):
    REQUIREMENTS.append('enum34')

setup(
    name='pyswmm',
    version=get_version(),
    description='Python Wrapper for SWMM5 API',
    long_description=get_description(),
    url='https://github.com/OpenWaterAnalytics/pyswmm/wiki',
    author='Bryant E. McDonnell (EmNet LLC)',
    author_email='bemcdonnell@gmail.com',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_data={'': ['lib/windows/swmm5.dll', 'LICENSE.txt']},
    include_package_data=True,
    license="BSD2 License",
    keywords="swmm5, swmm, hydraulics, hydrology, modeling, collection system",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Documentation :: Sphinx",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: C",
        "Development Status :: 4 - Beta",
    ])
