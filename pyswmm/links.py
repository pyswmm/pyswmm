# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Links module for the pythonic interface to SWMM5."""
from swmm.toolkit import shared_enum

# Local imports
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import LinkParams, LinkResults, LinkPollut, LinkType, ObjectType


class Links(object):
    """
    Link Iterator Methods.

    :param object model: Open Model Instance

    Examples:

    >>> from pyswmm import Simulation, Links
    >>>
    >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
    ...     for link in Links(sim):
    ...         print(link)
    ...         print(link.linkid)
    <swmm5.Link object at 0x031B0350>
    C1
    <swmm5.Link object at 0x030693D0>
    C2
    <swmm5.Link object at 0x031B0350>
    C3
    <swmm5.Link object at 0x030693D0>
    C0

    Iterating or Links Object

    >>> links = Links(sim)
    >>> for link in links:
    ...     print(link.linkid)
    C1:C2
    C2
    C3

    Testing Existence

    >>> links = Links(sim)
    >>> "C1:C2" in links
    True

    Initializing a link Object

    >>> links = Links(sim)
    >>> c1c2 = links['C1:C2']
    >>> c1c2.flow_limit = 12
    >>> c1c2.flow_limit
    12
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model
        self._cuindex = 0
        self._nLinks = self._model.getProjectSize(ObjectType.LINK.value)

    def __len__(self):
        """
        Return number of links. Use the expression 'len(Links)'.

        :return: Number of Links
        :rtype: int
        """
        return self._model.getProjectSize(ObjectType.LINK.value)

    def __contains__(self, linkid):
        """
        Checks if Link ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return self._model.ObjectIDexist(ObjectType.LINK.value, linkid)

    def __getitem__(self, linkid):
        if self.__contains__(linkid):
            ln = Link(self._model, linkid)
            _ln = ln
            if ln.is_conduit():
                _ln.__class__ = Conduit
            elif ln.is_pump():
                _ln.__class__ = Pump
            return _ln
        else:
            raise PYSWMMException("Link ID: {} Does not Exist".format(linkid))

    def __iter__(self):
        return self

    def __next__(self):
        if self._cuindex < self._nLinks:
            linkobject = self.__getitem__(self._linkid)
            self._cuindex += 1  # Next Iteration
            return linkobject
        else:
            raise StopIteration()

    @property
    def _linkid(self):
        """Link ID."""
        return self._model.getObjectId(ObjectType.LINK.value, self._cuindex)


class Link(object):
    """
    Link Methods.

    :param object model: Open Model Instance
    :param str linkid: Link ID

    Examples:

    >>> from pyswmm import Simulation, Links
    >>>
    >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
    ...     c1c2 = Links(sim)["C1:C2"]
    ...     print(c1c2.flow)
    ...     for step in sim:
    ...         print(c1c2.flow)
    0.0
    """

    def __init__(self, model, linkid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if linkid not in model.getObjectIDList(ObjectType.LINK.value):
            raise PYSWMMException("ID Not valid")
        self._model = model
        self._linkid = linkid

    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def linkid(self):
        """
        Get Link ID.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.linkid)
        "C1"
        """
        return self._linkid

    def is_conduit(self):
        """
        Check if link is a Conduit Type.

        :return: is conduit
        :rtype: bool

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.is_conduit())
        True
        """
        return self._model.getLinkType(self._linkid) is shared_enum.LinkType.CONDUIT

    def is_pump(self):
        """
        Check if link is a Pump Type.

        :return: is pump
        :rtype: bool

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.is_pump())
        False
        """
        return self._model.getLinkType(self._linkid) is shared_enum.LinkType.PUMP

    def is_orifice(self):
        """
        Check if link is a Orifice Type.

        :return: is orifie
        :rtype: bool

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.is_orifice())
        False
        """
        return self._model.getLinkType(self._linkid) is shared_enum.LinkType.ORIFICE

    def is_weir(self):
        """
        Check if link is a Weir Type.

        :return: is weir
        :rtype: bool

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.is_weir())
        False
        """
        return self._model.getLinkType(self._linkid) is shared_enum.LinkType.WEIR

    def is_outlet(self):
        """
        Check if link is a Outlet Type.

        :return: is outlet
        :rtype: bool

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.is_outlet())
        False
        """
        return self._model.getLinkType(self._linkid) is shared_enum.LinkType.OUTLET

    @property
    def connections(self):
        """
        Get link upstream and downstream node IDs.

        :return: ("UpstreamNodeID","DownstreamNodeID")
        :rtype: tuple

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.connections)
        ("C1","C2")
        """
        return self._model.getLinkConnections(self._linkid)

    @property
    def inlet_node(self):
        """
        Get link inlet node ID.

        :return: Inlet node ID
        :rtype: str

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.inlet_node)
        C1
        """
        return self._model.getLinkConnections(self._linkid)[0]

    @property
    def outlet_node(self):
        """
        Get link outlet node ID.

        :return: Outlet node ID
        :rtype: str

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.outlet_node)
        C2
        """
        return self._model.getLinkConnections(self._linkid)[1]

    @property
    def inlet_offset(self):
        """
        Get/set Upstream Offset Depth.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.inlet_offset)
        0.1

        Setting the value

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.inlet_offset)
        ...     c1c2.inlet_offset = 0.2
        ...     print(c1c2.inlet_offset)
        0.1
        0.2
        """
        return self._model.getLinkParam(self._linkid, LinkParams.offset1.value)

    @inlet_offset.setter
    def inlet_offset(self, param):
        """Set Link Upstream Link Offset."""
        self._model.setLinkParam(self._linkid, LinkParams.offset1.value, param)
    @property
    def outlet_offset(self):

        """
        Get/set Downstream Offset Depth.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.outlet_offset)
        0.1

        Setting the value

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.outlet_offset)
        ...     c1c2.outlet_offset = 0.2
        ...     print(c1c2.outlet_offset)
        0.1
        0.2
        """
        return self._model.getLinkParam(self._linkid, LinkParams.offset2.value)

    @outlet_offset.setter
    def outlet_offset(self, param):
        """Set Link Downstream Link Offset."""
        self._model.setLinkParam(self._linkid, LinkParams.offset2.value, param)

    @property
    def initial_flow(self):
        """
        Get/set Link Initial Flow.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.initial_flow)
        0

        Setting the Value

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.initial_flow)
        ...     c1c2.initial_flow = 0.2
        ...     print(c1c2.initial_flow)
        0.1
        0.2
        """
        return self._model.getLinkParam(self._linkid, LinkParams.q0.value)

    @initial_flow.setter
    def initial_flow(self, param):
        """Set Link Initial Flow Rate."""
        self._model.setLinkParam(self._linkid, LinkParams.q0.value, param)

    @property
    def flow_limit(self):
        """
        Get/set link flow limit.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.flow_limit)
        0

        Setting the Value

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.flow_limit)
        ...     c1c2.flow_limit = 0.2
        ...     print(c1c2.flow_limit)
        0
        0.2
        """
        return self._model.getLinkParam(self._linkid, LinkParams.qLimit.value)

    @flow_limit.setter
    def flow_limit(self, param):
        """Set Link Flow Limit."""
        self._model.setLinkParam(self._linkid, LinkParams.qLimit.value, param)

    @property
    def inlet_head_loss(self):
        """
        Get/set Inlet Head Loss.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.inlet_head_loss)
        0

        Setting the Value

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.inlet_head_loss)
        ...     c1c2.inlet_head_loss = 0.2
        ...     print(c1c2.inlet_head_loss)
        0
        0.2
        """
        return self._model.getLinkParam(self._linkid,
                                        LinkParams.cLossInlet.value)

    @inlet_head_loss.setter
    def inlet_head_loss(self, param):
        """Set Link Inlet Head Loss."""
        self._model.setLinkParam(self._linkid, LinkParams.cLossInlet.value,
                                 param)

    @property
    def outlet_head_loss(self):
        """
        Get/set Outlet Head Loss.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.outlet_head_loss)
        0

        Setting the Value

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.outlet_head_loss)
        ...     c1c2.outlet_head_loss = 0.2
        ...     print(c1c2.outlet_head_loss)
        0
        0.2
        """
        return self._model.getLinkParam(self._linkid,
                                        LinkParams.cLossOutlet.value)

    @outlet_head_loss.setter
    def outlet_head_loss(self, param):
        """Set Link Outlet Head Loss."""
        self._model.setLinkParam(self._linkid, LinkParams.cLossOutlet.value,
                                 param)

    @property
    def average_head_loss(self):
        """
        Get/set Average Conduit Loss.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.average_head_loss)
        0

        Setting the value

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.average_head_loss)
        ...     c1c2.average_head_loss = 0.2
        ...     print(c1c2.average_head_loss)
        0
        0.2
        """
        return self._model.getLinkParam(self._linkid,
                                        LinkParams.cLossAvg.value)

    @average_head_loss.setter
    def average_head_loss(self, param):
        """Set Link Average Head Loss."""
        self._model.setLinkParam(self._linkid, LinkParams.cLossAvg.value,
                                 param)

    @property
    def seepage_rate(self):
        """
        Get/set Conduit Seepage Loss.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.seepage_rate)
        0

        Setting the Value

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.seepage_rate)
        ...     c1c2.seepagerate = 0.2
        ...     print(c1c2.seepage_rate)
        0
        0.2
        """
        return self._model.getLinkParam(self._linkid,
                                        LinkParams.seepRate.value)

    @seepage_rate.setter
    def seepage_rate(self, param):
        """Set Link Average Seepage Loss."""
        self._model.setLinkParam(self._linkid, LinkParams.seepRate.value,
                                 param)

    @property
    def flow(self):
        """
        Get Link Results for Flow.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print(c1c2.flow)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getLinkResult(self._linkid,
                                         LinkResults.newFlow.value)

    @property
    def depth(self):
        """
        Get Link Results for Depth.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print(c1c2.depth)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getLinkResult(self._linkid,
                                         LinkResults.newDepth.value)

    @property
    def volume(self):
        """
        Get Link Results for Volume.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print(c1c2.volume)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getLinkResult(self._linkid,
                                         LinkResults.newVolume.value)

    @property
    def froude(self):
        """
        Get Link Results for Froude.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print(c1c2.froude)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getLinkResult(self._linkid,
                                         LinkResults.froude.value)

    @property
    def ups_xsection_area(self):
        """
        Get Link Results for Upstream X-section Flow Area.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print(c1c2.ups_xsection_area)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getLinkResult(self._linkid,
                                         LinkResults.surfArea1.value)

    @property
    def ds_xsection_area(self):
        """
        Get Link Results for Downstream X-section Flow Area.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print(c1c2.ds_xsection_area)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getLinkResult(self._linkid,
                                         LinkResults.surfArea2.value)

    @property
    def current_setting(self):
        """
        Get Link current setting.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print(c1c2.current_setting)
        0
        1
        0
        0.5
        1
        """
        return self._model.getLinkResult(self._linkid,
                                         LinkResults.setting.value)

    @property
    def target_setting(self):
        """
        Get/set Link Target Setting.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print(c1c2.target_setting)
        0
        0
        1
        0.5
        1

        Setting the Value

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print(c1c2.target_setting)
        ...         if c1c2.flow > 3:
        ...             c1c2.target_setting = 0.1
        0
        0
        0.1
        0.1
        0.1
        """
        return self._model.getLinkResult(self._linkid,
                                         LinkResults.targetSetting.value)

    @target_setting.setter
    def target_setting(self, setting):
        """
        Set Link Target Setting.

        If Simulation is not running this method will raise a warning and
        return 0.
        """
        return self._model.setLinkSetting(self._linkid, setting)

    @property
    def pollut_quality(self):
        """
        Get Current Water Quality Values for a Link.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Group of Water Quality Values.
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_pollutants.inp') as sim:
        ...     C1 = Links(sim)["C1"]
        ...     for step in sim:
        ...         print(C1.pollut_quality)
        {'test-pollutant': 0.0}
        {'test-pollutant': 120.0}
        {'test-pollutant': 120.0}
        """
        out_dict = {}
        pollut_ids = self._model.getObjectIDList(ObjectType.POLLUT.value)
        quality_array = self._model.getLinkPollut(self._linkid,
                                                      LinkPollut.linkQual.value)

        for ind in range(len(pollut_ids)):
            out_dict[pollut_ids[ind]] = quality_array[ind]

        return out_dict

    @pollut_quality.setter
    def pollut_quality(self, args):
        """
        Set Current Link Water Quality Value
        
        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_pollutants_setters.inp') as sim:
        ...     C1 = Links(sim)["C1"]
        ...     for step in sim:
        ...         C1.pollut_quality = ('test-pollutant', 100)
                    print(C1.pollut_quality)
        {'test-pollutant': 100.0}
        {'test-pollutant': 100.0}
        {'test-pollutant': 100.0}
        """

        pollutant_ID, pollutant_value = args

        self._model.setLinkPollut(self._linkid, pollutant_ID, pollutant_value)

    @property
    def total_loading(self):
        """
        Get Total Pollutant Loading Values for a Link.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Group of Total Loading Values.
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_pollutants.inp') as sim:
        ...     C1 = Links(sim)["C1"]
        ...     for step in sim:
        ...         print(C1.total_loading)
        {'test-pollutant': 0.01}
        {'test-pollutant': 0.02}
        {'test-pollutant': 0.03}
        """
        out_dict = {}
        pollut_ids = self._model.getObjectIDList(ObjectType.POLLUT.value)
        totalLoad_array = self._model.getLinkPollut(self._linkid,
                                                      LinkPollut.totalLoad.value)

        for ind in range(len(pollut_ids)):
            out_dict[pollut_ids[ind]] = totalLoad_array[ind]

        return out_dict

    @property
    def reactor_quality(self):
        """
        Get Current Water Quality Values for the mixed reactor inside a Link.
        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Group of Water Quality Values.
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Links
        >>>
        >>> with Simulation('tests/data/model_pollutants.inp') as sim:
        ...     C1 = Links(sim)["C1"]
        ...     for step in sim:
        ...         print(C1.reactor_quality)
        {'test-pollutant': 0.0}
        {'test-pollutant': 120.0}
        {'test-pollutant': 120.0}
        """
        out_dict = {}
        pollut_ids = self._model.getObjectIDList(ObjectType.POLLUT.value)
        quality_array = self._model.getLinkPollut(self._linkid,
                                                      LinkPollut.linkQual.value)

        for ind in range(len(pollut_ids)):
            out_dict[pollut_ids[ind]] = quality_array[ind]

        return out_dict


class Conduit(Link):
    """
    Conduit Object: Subclass of Link Object.
    """

    def __init__(self):
        super(Conduit, self).__init__()

    @property
    def conduit_statistics(self):
        """
        Conduit Flow Stats. The stats returned are rolling/cumulative.
        Indeces are as follows:

        +-----------------------+
        | peak_flow             |
        +-----------------------+
        | peak_flow_date        |
        +-----------------------+
        | peak_velocity         |
        +-----------------------+
        | peak_depth            |
        +-----------------------+
        | time_normal_flow      |
        +-----------------------+
        | time_inlet_control    |
        +-----------------------+
        | time_surcharged       |
        +-----------------------+
        | time_full_upstream    |
        +-----------------------+
        | time_full_downstream  |
        +-----------------------+
        | time_full_flow        |
        +-----------------------+
        | time_capacity_limited |
        +-----------------------+
        | time_in_flow_class    |
        +-----------------------+
        | time_courant_crit     |
        +-----------------------+
        | flow_turns            |
        +-----------------------+
        | flow_turn_sign        |
        +-----------------------+

        Time in Flow Class: (Fraction of Total Time)

        +-----+--------+----------+----------+----------+---------+-----------+
        | 0   | 1      | 2        | 3        | 4        | 5       | 6         |
        +-----+--------+----------+----------+----------+---------+-----------+
        | Dry | Up Dry | Down Dry | Sub Crit | Sup Crit | Up Crit | Down Crit |
        +-----+--------+----------+----------+----------+---------+-----------+

        :return: Group of Stats
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Links
        >>> import pprint
        >>> pp = pprint.PrettyPrinter(indent=4)
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:        
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print(c1c2.flow)
        ...     for step in sim:
        ...         pass
        ...     pp.pprint(c1c2.conduit_statistics)        
        o  Retrieving project data
        {   'flow_turn_sign': -1,
            'flow_turns': 1,
            'peak_depth': 0.8744979811226141,
            'peak_flow': 9.612897240188659,
            'peak_flow_date': 42310.00000579861,
            'peak_velocity': 13.200109870715737,
            'time_capacity_limited': 0.0,
            'time_courant_crit': 0.0,
            'time_full_downstream': 0.0,
            'time_full_flow': 57.98847222222222,
            'time_full_upstream': 57.98902777777778,
            'time_in_flow_class': <Swig Object of type 'DateTime *' at 0x7f7d591269a0>,
            'time_inlet_control': 0.0,
            'time_normal_flow': 0.0001388888888888889,
            'time_surcharged': 0.0
        }

        """
        return self._model.conduit_statistics(self.linkid)


class Pump(Link):
    """
    Pump Object: Subclass of Link Object.
    """

    def __init__(self):
        super(Pump, self).__init__()

    @property
    def pump_statistics(self):
        """
        Pump Stats. The stats returned are rolling/cumulative.
        Indeces are as follows:

        +------------------+
        | percent_utilized |
        +------------------+
        | min_flowrate     |
        +------------------+
        | average_flowrate |
        +------------------+
        | max_flowrate     |
        +------------------+
        | total_volume     |
        +------------------+
        | energy_consumed  |
        +------------------+
        | off_curve_low    |
        +------------------+
        | off_curve_high   |
        +------------------+
        | number_startups  |
        +------------------+
        | total_periods    |
        +------------------+

        :return: Group of Stats
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Links
        >>> import pprint
        >>> pp = pprint.PrettyPrinter(indent=4)
        >>>        
        >>> with Simulation('tests/data/model_pump_setting.inp') as sim:        
        ...     c3 = Links(sim)["C3"]
        ...     for step in sim:
        ...         pass
        ...     pp.pprint(c3.pump_statistics)        
        o  Retrieving project data
        {   'average_flowrate': 20.0,
            'energy_consumed': 2792.5975765384896,
            'max_flowrate': 20.0,
            'min_flowrate': 0.0,
            'number_startups': 1,
            'off_curve_high': 0.0,
            'off_curve_low': 0.0,
            'percent_utilized': 208800.0,
            'total_periods': 208801,
            'total_volume': 4176000.0
        }
        """
        return self._model.pump_statistics(self.linkid)
