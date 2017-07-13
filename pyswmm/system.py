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
        Get rolling/cumulative routing stats. Follow Data are returned:

        +-------------------------+
        | DWF Inflow Volume       |
        +-------------------------+
        | WWF Inflow Volume       |
        +-------------------------+
        | GW Inflow Volume        |
        +-------------------------+
        | I&I Inflow Volume       |
        +-------------------------+
        | External Inflow Volume  |
        +-------------------------+
        | Flooding Volume         |
        +-------------------------+
        | Outflow Volume          |
        +-------------------------+
        | Evaporation Loss Volume |
        +-------------------------+
        | Seepage Loss Volume     |
        +-------------------------+
        | Routing Error (%)       |
        +-------------------------+

        :return: Statistics
        :rtype: dict
        """
        return self._model.flow_routing_stats()

    @property
    def runoff_stats(self):
        """
        Get rolling/cumulative runoff stats. Follow Data are returned:

        +-----------------------+
        | Total Precipitation   |
        +-----------------------+
        | Evaporation Volume    |
        +-----------------------+
        | Infiltration Volume   |
        +-----------------------+
        | Runoff Volume         |
        +-----------------------+
        | Runon Volume          |
        +-----------------------+
        | Drain Volume          |
        +-----------------------+
        | Snow Removed Volume   |
        +-----------------------+
        | Initial Stored Volume |
        +-----------------------+
        | Initial Snow Volume   |
        +-----------------------+
        | Runoff Routing Error  |
        +-----------------------+

        :return: Statistics
        :rtype: dict
        """
        return self._model.runoff_routing_stats()
