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

    >>> from pyswmm import Simulation, SystemStats
    >>>
    >>> with Simulation('tests/data/TestModel1_weirSetting.inp') as sim:
    ...     system_routing = SystemStats(sim)
    ...
    ...     for step in sim:
    ...         print(system_routing.routing_stats)
    ...         print(system_routing.runoff_stats)
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

        +--------------------+
        | dry_weather_inflow |
        +--------------------+
        | wet_weather_inflow |
        +--------------------+
        | groundwater_inflow |
        +--------------------+
        | II_inflow          |
        +--------------------+
        | external_inflow    |
        +--------------------+
        | flooding           |
        +--------------------+
        | outflow            |
        +--------------------+
        | evaporation_loss   |
        +--------------------+
        | seepage_loss       |
        +--------------------+
        | reacted            |
        +--------------------+
        | initial_storage    |
        +--------------------+
        | final_storage      |
        +--------------------+
        | routing_error      |
        +--------------------+

        :return: Statistics
        :rtype: dict
        """
        return self._model.flow_routing_stats()

    @property
    def runoff_stats(self):
        """
        Get rolling/cumulative runoff stats. Follow Data are returned:

        +------------------+
        | rainfall         |
        +------------------+
        | evaporation      |
        +------------------+
        | infiltration     |
        +------------------+
        | runoff           |
        +------------------+
        | drains           |
        +------------------+
        | runon            |
        +------------------+
        | init_storage     |
        +------------------+
        | final_storage    |
        +------------------+
        | init_snow_cover  |
        +------------------+
        | final_snow_cover |
        +------------------+
        | snow_removed     |
        +------------------+
        | routing_error    |
        +------------------+

        :return: Statistics
        :rtype: dict
        """
        return self._model.runoff_routing_stats()
