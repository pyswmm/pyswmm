# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Nodes module for the pythonic interface to SWMM5."""
from swmm.toolkit import shared_enum

# Local imports
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import NodeParams, NodeResults, NodePollut, NodeType, ObjectType


class Nodes(object):
    """
    Node Iterator Methods.

    :param object model: Open Model Instance

    Examples:

    >>> from pyswmm import Simulation, Nodes
    >>>
    >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
    ...     for node in Nodes(sim):
    ...         print(node)
    ...         print(node.nodeid)
    <swmm5.Node object at 0x031B0350>
    J1
    <swmm5.Node object at 0x030693D0>
    J2
    <swmm5.Node object at 0x031B0350>
    J3
    <swmm5.Node object at 0x030693D0>
    J0

    Iterating over Nodes Object

    >>> nodes = Nodes(sim)
    >>> for node in nodes:
    ...     print(node.nodeid)
    J0
    J1
    J2
    J3

    Testing Existence

    >>> nodes = Nodes(sim)
    >>> "J1" in nodes
    True

    Initializing a node Object

    >>> nodes = Nodes(sim)
    >>> j1 = nodes['J1']
    >>> print(j1.invert_elevation)
    12
    >>>
    >>> j1.invert_elevation = 200
    >>> print(j1.invert_elevation)
    200
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model
        self._cuindex = 0
        self._nNodes = self._model.getProjectSize(ObjectType.NODE.value)

    def __len__(self):
        """
        Return number of nodes. Use the expression 'len(Nodes)'.

        :return: Number of Nodes
        :rtype: int

        """
        return self._model.getProjectSize(ObjectType.NODE.value)

    def __contains__(self, nodeid):
        """
        Checks if Node ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return self._model.ObjectIDexist(ObjectType.NODE.value, nodeid)

    def __getitem__(self, nodeid):
        if self.__contains__(nodeid):
            nd = Node(self._model, nodeid)
            _nd = nd
            if nd.is_outfall():
                _nd.__class__ = Outfall
            elif nd.is_storage():
                _nd.__class__ = Storage
            return _nd

        else:
            raise PYSWMMException("Node ID: {} Does not Exist".format(nodeid))

    def __iter__(self):
        return self

    def __next__(self):
        if self._cuindex < self._nNodes:
            nodeobject = self.__getitem__(self._nodeid)
            self._cuindex += 1  # Next Iteration
            return nodeobject
        else:
            raise StopIteration()

    @property
    def _nodeid(self):
        """Node ID."""
        return self._model.getObjectId(ObjectType.NODE.value, self._cuindex)


class Node(object):
    """
    Node Methods.

    :param object model: Open Model Instance
    :param str nodeid: Node ID

    Examples:

    >>> from pyswmm import Simulation, Nodes
    >>>
    >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
    ...     j1 = Nodes(sim)["J1"]
    ...     print(j1.invert_el)
    ...     for step in sim:
    ...         print(j1.depth)
    0.0
    """

    def __init__(self, model, nodeid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if nodeid not in model.getObjectIDList(ObjectType.NODE.value):
            raise PYSWMMException("ID Not valid")
        self._model = model
        self._nodeid = nodeid

    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def nodeid(self):
        """
        Get Node ID.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.nodeid)
        J1
        """
        return self._nodeid

    def is_junction(self):
        """
        Check if node is a Junction Type.

        :return: is junction
        :rtype: bool

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.is_junction())
        True
        """
        return self._model.getNodeType(self._nodeid) is shared_enum.NodeType.JUNCTION

    def is_outfall(self):
        """
        Check if node is a Outfall Type.

        :return: is outfall
        :rtype: bool

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.is_outfall())
        True
        """
        return self._model.getNodeType(self._nodeid) is shared_enum.NodeType.OUTFALL

    def is_storage(self):
        """
        Check if node is a Storage Type.

        :return: is storage
        :rtype: bool

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.is_storage())
        True
        """
        return self._model.getNodeType(self._nodeid) is shared_enum.NodeType.STORAGE

    def is_divider(self):
        """
        Check if node is a Divider Type.

        :return: is divider
        :rtype: bool

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.is_divider())
        True
        """
        return self._model.getNodeType(self._nodeid) is shared_enum.NodeType.DIVIDER

    @property
    def invert_elevation(self):
        """
        Get/set node invert elevation.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.invert_elevation)
        0.1

        Setting the value

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.invert_elevation)
        ...     j1.invert_elevation = 0.2
        ...     print(j1.invert_elevation)
        0.1
        0.2
        """
        return self._model.getNodeParam(self._nodeid,
                                        NodeParams.invertElev.value)

    @invert_elevation.setter
    def invert_elevation(self, param):
        """Set Node Invert Elevation."""
        self._model.setNodeParam(self._nodeid, NodeParams.invertElev.value,
                                 param)

    @property
    def full_depth(self):
        """
        Get node full depth (Physical Depth of manhole).

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.full_depth)
        10

        Setting the value

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.full_depth)
        ...     j1.full_depth = 50
        ...     print(j1.full_depth)
        10
        50
        """
        return self._model.getNodeParam(self._nodeid,
                                        NodeParams.fullDepth.value)

    @full_depth.setter
    def full_depth(self, param):
        """Set Node Full Depth."""
        self._model.setNodeParam(self._nodeid, NodeParams.fullDepth.value,
                                 param)

    @property
    def surcharge_depth(self):
        """
        Get/set node surcharge depth.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.surcharge_depth)
        10

        Setting the value

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.surcharge_depth)
        ...     j1.surcharge_depth = 50
        ...     print(j1.surcharge_depth)
        10
        50
        """
        return self._model.getNodeParam(self._nodeid,
                                        NodeParams.surDepth.value)

    @surcharge_depth.setter
    def surcharge_depth(self, param):
        """Set Node Surcharge Depth."""
        self._model.setNodeParam(self._nodeid, NodeParams.surDepth.value,
                                 param)

    @property
    def ponding_area(self):
        """
        Get/set node ponding area.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.ponding_area)
        0

        Setting the value

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.ponding_area)
        ...     j1.ponding_area = 50
        ...     print(j1.ponding_area)
        0
        50
        """
        return self._model.getNodeParam(self._nodeid,
                                        NodeParams.pondedArea.value)

    @ponding_area.setter
    def ponding_area(self, param):
        """Set Node Ponding Area."""
        self._model.setNodeParam(self._nodeid, NodeParams.pondedArea.value,
                                 param)

    @property
    def initial_depth(self):
        """
        Get/set node initial depth.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.initial_depth)
        0

        Setting the value

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     print(j1.initial_depth)
        ...     j1.initial_depth = 1
        ...     print(j1.initial_depth)
        0
        1
        """
        return self._model.getNodeParam(self._nodeid,
                                        NodeParams.initDepth.value)

    @initial_depth.setter
    def initial_depth(self, param):
        """Set Node Initial Depth."""
        self._model.setNodeParam(self._nodeid, NodeParams.initDepth.value,
                                 param)

    @property
    def total_inflow(self):
        """
        Get Node Results for Total Inflow Rate.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(j1.total_inflow)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getNodeResult(self._nodeid,
                                         NodeResults.totalinflow.value)

    @property
    def total_outflow(self):
        """
        Get Node Results for Total Outflow Rate.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(j1.total_outflow)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getNodeResult(self._nodeid,
                                         NodeResults.outflow.value)

    @property
    def losses(self):
        """
        Get Node Results for Losses Rate (Evap and Exfiltration).

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(j1.losses)
        0
        0.01
        0.01
        0.01
        0.01
        """
        return self._model.getNodeResult(self._nodeid,
                                         NodeResults.losses.value)

    @property
    def volume(self):
        """
        Get Node Results for Volume.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(j1.volume)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getNodeResult(self._nodeid,
                                         NodeResults.newVolume.value)

    @property
    def flooding(self):
        """
        Get Node Results for Flooding Rate.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(j1.flooding)
        0
        0
        0.01
        0
        0
        """
        return self._model.getNodeResult(self._nodeid,
                                         NodeResults.overflow.value)

    @property
    def depth(self):
        """
        Get Node Results for Depth.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(j1.depth)
        0
        0.5
        0.51
        0.52
        0.49
        """
        return self._model.getNodeResult(self._nodeid,
                                         NodeResults.newDepth.value)

    @property
    def head(self):
        """
        Get Node Results for Head.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(j1.head)
        10
        10.5
        10.51
        10.52
        10.49
        """
        return self._model.getNodeResult(self._nodeid,
                                         NodeResults.newHead.value)

    @property
    def lateral_inflow(self):
        """
        Get Node Results for lateral Inflow rate.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(j1.lateral_inflow)
        0
        0.25
        0.25
        0.3
        0.4
        """
        return self._model.getNodeResult(self._nodeid,
                                         NodeResults.newLatFlow.value)

    @property
    def hydraulic_retention_time(self):
        """
        Get Node Results for hydraulic retention time.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float
        """
        return self._model.getNodeResult(self._nodeid,
                                         NodeResults.hyd_res_time.value)

    def generated_inflow(self, inflowrate):
        """
        Generate and Set a Node Inflow Rate.

        The value is held constant in the model until it is redefined.
        Generated inflows work like any SWMM inflow.  This does not
        introduce any continuity errors since all flows is counted as
        an inflow.

        :param float inflowrate: Inflow Rate

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         j1.generated_inflow(9)
        >>>
        """
        self._model.setNodeInflow(self._nodeid, inflowrate)

    @property
    def cumulative_inflow(self):
        """
        Get Cumulative Node Loading.

        :return: Cumulative Volume
        :rtype: float
        """
        value = self._model.node_inflow(self.nodeid)
        return value

    @property
    def pollut_quality(self):
        """
        Get Current Water Quality Values for a Node.
        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Group of Water Quality Values.
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/test_pollutants.inp') as sim:
        ...     J1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(J1.pollut_quality)
        {'test-pollutant': 0.0}
        {'test-pollutant': 120.0}
        {'test-pollutant': 120.0}
        """
        out_dict = {}
        pollut_ids = self._model.getObjectIDList(ObjectType.POLLUT.value)
        quality_array = self._model.getNodePollut(self._nodeid,
                                                      NodePollut.nodeQual.value)

        for ind in range(len(pollut_ids)):
            out_dict[pollut_ids[ind]] = quality_array[ind]

        return out_dict

    @pollut_quality.setter
    def pollut_quality(self, args):
        """
        Set Current Node Water Quality Value
        
        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/test_pollutants.inp') as sim:
        ...     Tank = Nodes(sim)["Tank"]
        ...     for step in sim:
        ...         Tank.pollut_quality = ('test-pollutant', 100)
                    print(Tank.pollut_quality)
        {'test-pollutant': 100.0}
        {'test-pollutant': 100.0}
        {'test-pollutant': 100.0}
        """
        pollutant_ID, pollutant_value = args
        
        self._model.setNodePollut(self._nodeid, pollutant_ID, pollutant_value)

    @property
    def inflow_quality(self):
        """
        Get Current Inflow Water Quality Values for a Node.
        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Group of Water Quality Values.
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/test_pollutants.inp') as sim:
        ...     J1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(J1.inflow_quality)
        {'test-pollutant': 0.0}
        {'test-pollutant': 120.0}
        {'test-pollutant': 120.0}
        """
        out_dict = {}
        pollut_ids = self._model.getObjectIDList(ObjectType.POLLUT.value)
        quality_array = self._model.getNodePollut(self._nodeid,
                                                      NodePollut.inflowQual.value)

        for ind in range(len(pollut_ids)):
            out_dict[pollut_ids[ind]] = quality_array[ind]

        return out_dict

    @property
    def reactor_quality(self):
        """
        Get Current Water Quality Values for the mixed reactor inside a Node.
        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Group of Water Quality Values.
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/test_pollutants.inp') as sim:
        ...     J1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         print(J1.reactor_quality)
        {'test-pollutant': 0.0}
        {'test-pollutant': 120.0}
        {'test-pollutant': 120.0}
        """
        out_dict = {}
        pollut_ids = self._model.getObjectIDList(ObjectType.POLLUT.value)
        quality_array = self._model.getNodePollut(self._nodeid,
                                                      NodePollut.reactorQual.value)

        for ind in range(len(pollut_ids)):
            out_dict[pollut_ids[ind]] = quality_array[ind]

        return out_dict

    @property
    def statistics(self):
        """
        Node Statistics. The stats returned are rolling/cumulative.
        Indeces are as follows:

        +-------------------------+
        | average_depth           |
        +-------------------------+
        | max_depth               |
        +-------------------------+
        | max_depth_date          |
        +-------------------------+
        | max_report_depth        |
        +-------------------------+
        | flooding_volume         |
        +-------------------------+
        | flooding_duration       |
        +-------------------------+
        | surcharge_duration      |
        +-------------------------+
        | courant_crit_duration   |
        +-------------------------+
        | lateral_inflow_vol      |
        +-------------------------+
        | peak_lateral_inflowrate |
        +-------------------------+
        | peak_total_inflow       |
        +-------------------------+
        | peak_flooding_rate      |
        +-------------------------+
        | max_ponded_volume       |
        +-------------------------+
        | max_inflow_date         |
        +-------------------------+
        | max_flooding_date       |
        +-------------------------+

        :return: Group of Stats
        :rtype: dict
        """
        return self._model.node_statistics(self.nodeid)


class Outfall(Node):
    """
    Outfall Object: Subclass of Node Object.
    """

    def __init__(self):
        super(Outfall, self).__init__()

    @property
    def outfall_statistics(self):
        """
        Outfall Stats. The stats returned are rolling/cumulative.
        Indeces are as follows:

        +-------------------+
        | average_flowrate  |
        +-------------------+
        | peak_flowrate     |
        +-------------------+
        | pollutant_loading |
        +-------------------+
        | total_periods     |
        +-------------------+

        :return: Group of Stats
        :rtype: list
        """
        return self._model.outfall_statistics(self.nodeid)

    def outfall_stage(self, stage):
        """
        Generate and Set an Outfall Stage (head).

        The value is held constant in the model until it is redefined.
        Using the function overrides the mechanism within SWMM that would
        internerally set the outfall stage.  This does not
        introduce any continuity errors since all flows is counted as
        an inflow.

        :param float stage: Outfall Stage (Head)

        Examples:

        >>> from pyswmm import Simulation, Nodes
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     j1 = Nodes(sim)["J1"]
        ...     for step in sim:
        ...         j1.outfall_stage(9)
        """
        self._model.setOutfallStage(self._nodeid, stage)


class Storage(Node):
    """
    Storage Object: Subclass of Node Object.
    """

    def __init__(self):
        super(Storage, self).__init__()

    @property
    def storage_statistics(self):
        """
        Storage Stats. The stats returned are rolling/cumulative.
        Indeces are as follows:

        +----------------+
        | initial_volume |
        +----------------+
        | average_volume |
        +----------------+
        | max_volume     |
        +----------------+
        | peak_flowrate  |
        +----------------+
        | evap_loss      |
        +----------------+
        | exfil_loss     |
        +----------------+
        | max_vol_date   |
        +----------------+

        :return: Group of Stats
        :rtype: list
        """
        return self._model.storage_statistics(self.nodeid)
