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
from pyswmm.toolkitapi import SysRoutingStats, SysRunoffStats


class FlowRouting(object):
    """
    System-Wide Flow Routing Accumulation Volume Methods.

    :param object model: Open Model Instance

    Examples:

    >>> from pyswmm import Simulation, SystemFlowRouting
    >>>
    >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
    ...     system_routing = FlowRouting(sim)
    ...     print system_routing.wet_weather_inflow
    ...
    ...     for step in simulation:
    ...         print system_routing.wet_weather_inflow
    ... 0.0
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model

    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def dry_weather_inflow(self):
        """
        Get cumulative dry weather inflow volume.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_flow_routing(SysRoutingStats.DWinflow.value)

    @property
    def wet_weather_inflow(self):
        """
        Get cumulative wet weather inflow volume.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_flow_routing(SysRoutingStats.WWinflow.value)

    @property
    def groundwater_inflow(self):
        """
        Get cumulative groundwater inflow volume.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_flow_routing(SysRoutingStats.GWinflow.value)

    @property
    def iandi_inflow(self):
        """
        Get cumulative I&I inflow volume.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_flow_routing(SysRoutingStats.IIinflow.value)

    @property
    def external_inflow(self):
        """
        Get cumulative external inflow volume.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_flow_routing(SysRoutingStats.EXinflow.value)

    @property
    def flooding(self):
        """
        Get cumulative flooding volume.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_flow_routing(SysRoutingStats.flooding.value)

    @property
    def outfall_loading(self):
        """
        Get cumulative outfall volume.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_flow_routing(SysRoutingStats.outfall.value)

    @property
    def evaporation(self):
        """
        Get cumulative evaporation volume.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_flow_routing(
            SysRoutingStats.evaporation.value)

    @property
    def seepage(self):
        """
        Get cumulative seepage volume.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_flow_routing(SysRoutingStats.seepage.value)

    @property
    def routing_error(self):
        """
        Get current routing error.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_flow_routing(
            SysRoutingStats.routing_error.value)


class RunoffRouting(object):
    """
    System-wide Runoff Routing Accumulation Volume Methods.

    :param object model: Open Model Instance

    Examples:

    >>> from pyswmm import Simulation, SystemRunoffRouting
    >>>
    >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
    ...     sys_ro_route = RunoffRouting(sim)
    ...     print sys_ro_route.rainfall
    ...
    ...     for step in simulation:
    ...         print sys_ro_route.rainfall
    ... 0.0
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model

    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def rainfall(self):
        """
        Get cumulative rainfall (Units: in or mm).

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_runoff_routing(SysRunoffStats.rainfall.value)

    @property
    def evaporation(self):
        """
        Get cumulative evaporation (Units: in or mm).

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_runoff_routing(
            SysRunoffStats.evaporation.value)

    @property
    def infiltration(self):
        """
        Get cumulative infiltration (Units: in or mm).

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_runoff_routing(
            SysRunoffStats.infiltration.value)

    @property
    def runoff(self):
        """
        Get cumulative runoff (Units: in or mm).

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_runoff_routing(SysRunoffStats.runoff.value)

    @property
    def runon(self):
        """
        Get cumulative runon (Units: in or mm).

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_runoff_routing(SysRunoffStats.runon.value)

    @property
    def drains(self):
        """
        Get cumulative drain (Units: in or mm).

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_runoff_routing(SysRunoffStats.drains.value)

    @property
    def snow_removed(self):
        """
        Get cumulative snow removed (Units: in or mm).

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_runoff_routing(
            SysRunoffStats.snow_removed.value)

    @property
    def initial_storage(self):
        """
        Get initial storage (Units: in or mm).

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_runoff_routing(
            SysRunoffStats.initial_storage.value)

    @property
    def initial_snow_cover(self):
        """
        Get inital snow cover (Units: in or mm).

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_runoff_routing(
            SysRunoffStats.initial_snow_cover.value)

    @property
    def routing_error(self):
        """
        Get current routing error.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.system_runoff_routing(
            SysRunoffStats.routing_error.value)
