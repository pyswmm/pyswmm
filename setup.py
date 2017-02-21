# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Python setup.py installer script."""

# Standard library imports
import sys

# Third party imports
from setuptools import find_packages, setup

PY2 = sys.version_info.major == 2
VERSION = '0.2.1'

REQUIREMENTS = []

if PY2:
    REQUIREMENTS.append('enum34')

setup(
    name='pyswmm',
    version=VERSION,
    description='Python Wrapper for SWMM5 API',
    url='https://github.com/OpenWaterAnalytics/pyswmm/wiki',
    author='Bryant E. McDonnell (EmNet LLC)',
    author_email='bemcdonnell@gmail.com',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_data={'': ['swmmLinkedLibs/Windows/swmm5.dll', 'LICENSE.txt']},
    include_package_data=True,
    license="BSD2 License",
    keywords="swmm5, swmm, hydraulics, hydrology, modeling, collection system",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Documentation :: Sphinx",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: C",
        "Development Status :: 4 - Beta",
    ])
