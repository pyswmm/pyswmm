# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2024 Bryant E. McDonnell (See AUTHORS)
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Python Wrapper for Stormwater Management Model (SWMM5)."""

# Local imports
import pyswmm._monkey_patch
from pyswmm.links import Link, Links
from pyswmm.lidcontrols import LidControls, LidControl
from pyswmm.lidgroups import LidGroups, LidGroup, LidUnit
from pyswmm.nodes import Node, Nodes
from pyswmm.simulation import Simulation, SimulationPreConfig
from pyswmm.output import Output, SubcatchSeries, NodeSeries, LinkSeries, SystemSeries
from pyswmm.subcatchments import Subcatchment, Subcatchments
from pyswmm.system import SystemStats
from pyswmm.raingages import RainGages, RainGage

VERSION_INFO = (2, 0, 1)

__version__ = ".".join(map(str, VERSION_INFO))
__author__ = "Bryant E. McDonnell (Hydroinformatics, LLC) - bemcdonnell@gmail.com"
__copyright__ = "Copyright (c) 2024 Bryant E. McDonnell (See AUTHORS)"
__licence__ = "BSD2"
__all__ = [
    Link,
    Links,
    LidControls,
    LidGroups,
    Node,
    Nodes,
    Subcatchment,
    Subcatchments,
    Simulation,
    SimulationPreConfig,
    SystemStats,
    RainGages,
    RainGage,
    Output,
    SubcatchSeries,
    NodeSeries,
    LinkSeries,
    SystemSeries,
]


# Monkey Patching
pyswmm._monkey_patch.patch()
