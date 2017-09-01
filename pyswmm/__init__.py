# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Python Wrapper for Stormwater Management Model (SWMM5)."""

# Local imports
from pyswmm.links import Link, Links
from pyswmm.nodes import Node, Nodes
from pyswmm.simulation import Simulation
from pyswmm.subcatchments import Subcatchment, Subcatchments
from pyswmm.system import SystemStats

<<<<<<< 17520bd7dfbf1b20865f2a7f114e119d3d8b4614

VERSION_INFO = (0, 4, 4, 'dev0')
=======
VERSION_INFO = (0, 5, 0, 'dev0')
>>>>>>> ciocheck
__version__ = '.'.join(map(str, VERSION_INFO))
__swmm_version__ = '5.2.0.dev0'
__author__ = 'Bryant E. McDonnell (EmNet LLC) - bemcdonnell@gmail.com'
__copyright__ = 'Copyright (c) 2016 Bryant E. McDonnell (PySWMM Developers)'
__licence__ = 'BSD2'
__all__ = [
    Link, Links, Node, Nodes, Subcatchment, Subcatchments, Simulation,
    SystemStats
]
