# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""System module for the pythonic interface to SWMM5."""

# Local imports
from pyswmm.swmm5 import PYSWMMException
import pyswmm.toolkitapi as tka


class SystemStats(object):
    """
    System-Wide Flow and Runoff Routing Accumulation Volume Methods.

    :param object model: Open Model Instance

    Examples:

    >>> from pyswmm import Simulation, SystemFlowRouting
    >>>
    >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
    ...     system_routing = SystemStats(sim)
    ...
    ...     for step in simulation:
    ...         print system_routing.routing_stats
    ...         print system_routing.runoff_stats
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model

    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def routing_stats(self):
        """
        Get rolling/cumulative routing stats. Indeces represent the following:

        +-------------------------+---+
        | DWF Inflow Volume       | 0 |
        +-------------------------+---+
        | WWF Inflow Volume       | 1 |
        +-------------------------+---+
        | GW Inflow Volume        | 2 |
        +-------------------------+---+
        | I&I Inflow Volume       | 3 |
        +-------------------------+---+
        | External Inflow Volume  | 4 |
        +-------------------------+---+
        | Flooding Volume         | 5 |
        +-------------------------+---+
        | Outflow Volume          | 6 |
        +-------------------------+---+
        | Evaporation Loss Volume | 7 |
        +-------------------------+---+
        | Seepage Loss Volume     | 8 |
        +-------------------------+---+
        | Routing Error (%)       | 9 |
        +-------------------------+---+        

        :return: Statistics
        :rtype: list
        """
        return self._model.system_statistics(
            tka.SystemStats.sys_flow_routing.value)

    @property
    def runoff_stats(self):
        """
        Get rolling/cumulative runoff stats. Indeces represent the following:

        +-----------------------+---+
        | Total Precipitation   | 0 |
        +-----------------------+---+
        | Evaporation Volume    | 1 |
        +-----------------------+---+
        | Infiltration Volume   | 2 |
        +-----------------------+---+
        | Runoff Volume         | 3 |
        +-----------------------+---+
        | Runon Volume          | 4 |
        +-----------------------+---+
        | Drain Volume          | 5 |
        +-----------------------+---+
        | Snow Removed Volume   | 6 |
        +-----------------------+---+
        | Initial Stored Volume | 7 |
        +-----------------------+---+
        | Initial Snow Volume   | 8 |
        +-----------------------+---+
        | Runoff Routing Error  | 9 |
        +-----------------------+---+

        :return: Statistics
        :rtype: list
        """
        return self._model.system_statistics(
            tka.SystemStats.sys_runoff_routing.value)
