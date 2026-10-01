# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2024 Bryant E. McDonnell (See AUTHORS)
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Python Wrapper for Stormwater Management Model (SWMM5)."""

# Local imports
import importlib.metadata

import pyswmm._monkey_patch
from pyswmm.lidcontrols import LidControl, LidControls
from pyswmm.lidgroups import LidGroup, LidGroups, LidUnit
from pyswmm.links import Link, Links
from pyswmm.nodes import Node, Nodes
from pyswmm.output import LinkSeries, NodeSeries, Output, SubcatchSeries, SystemSeries
from pyswmm.raingages import RainGage, RainGages
from pyswmm.simulation import Simulation, SimulationPreConfig
from pyswmm.subcatchments import Subcatchment, Subcatchments
from pyswmm.system import SystemStats

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development mode

__author__ = "Bryant E. McDonnell (Hydroinformatics, LLC) - bemcdonnell@gmail.com"
__copyright__ = "Copyright (c) 2025 Bryant E. McDonnell (See AUTHORS)"
__licence__ = "BSD2"
__all__ = [
    "LidControl",
    "LidControls",
    "LidGroup",
    "LidGroups",
    "LidUnit",
    "Link",
    "LinkSeries",
    "Links",
    "Node",
    "NodeSeries",
    "Nodes",
    "Output",
    "RainGage",
    "RainGages",
    "Simulation",
    "SimulationPreConfig",
    "SubcatchSeries",
    "Subcatchment",
    "Subcatchments",
    "SystemSeries",
    "SystemStats",
]


# Monkey Patching
pyswmm._monkey_patch.patch()
