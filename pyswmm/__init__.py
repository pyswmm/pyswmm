# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Python Wrapper for Stormwater Management Model (SWMM5)."""

VERSION_INFO = (0, 3, 'dev0')
__version__ = '.'.join(map(str, VERSION_INFO))
__author__ = 'Bryant E. McDonnell (EmNet LLC) - bemcdonnell@gmail.com'
__copyright__ = 'Copyright (c) 2016 Bryant E. McDonnell'
__licence__ = 'BSD2'

from pyswmm.simulation import Simulation
from pyswmm.links import Links, Link
from pyswmm.nodes import Nodes, Node
