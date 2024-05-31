# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2018 Jennifer Wu
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
from pyswmm.swmm5 import PYSWMMException
from pyswmm import LidControls
from pyswmm.toolkitapi import ObjectType, LidUParams, LidUOptions, LidResults
from pyswmm.lidunits import Surface, Pavement, Soil, Storage, WaterBalance


class LidGroups(object):
    """
    LidGroups Iterator Methods.

    :param object model: Open Model Instance

    This allows the user to iterate and get one of the LID Groups as
    defined inside SWMM's [LID_USAGE] section.  For example, here is a sample
    section from a SWMM INP file.

    .. code-block::

        [LID_USAGE]
        ;;Subcatchment   LID Process   Number  Area    Width   InitSat  FromImp  ToPerv   RptFile  DrainTo  FromPerv
        ;;-------------- ------------- ------- ------- ------- -------- -------- -------- -------- -------- ----------
        J1_J3_qqqqqqq    LID_C1        1       180.00  2       0        0        0        *        *        0
        J11_J14_qqqqqqq  LID_C1        1       140     2       0        0        0        *        *        0


    Now we can peform manipulations in PySWMM and get objects.

    .. code-block:: python

        from pyswmm import Simulation, LidGroups

        with Simulation('lid_model.inp') as sim:
            for lid_group in LidGroups(sim):
                print(lid_group)

    .. code-block::

        >>> J1_J3_qqqqqqq
        >>> J11_J14_qqqqqqq

    Once a handle has been created of an LidGroup object we can now make
    adjustments to the parameters and change the behavior.  The following example
    provides some context around the different object handles created.  One
    feature presented herein shows that during a simulation the drain_node
    (or drain subcatchement) can be changed during the simulation.

    .. code-block:: python

        from pyswmm import Simulation, LidGroups

        with Simulation('lid_model.inp') as sim:
            # This returns an LidGroup object
            lid_group_j1_j3 = LidGroups(sim)["J1_J3_qqqqqqq"]

            # Next to get access to one of the LID units
            # inside this subcatchment it is indexed.

            # This returns an LidUnit object
            lid_unit0=lid_group_j1_j3[0]

            for ind, step in enumerate(sim):
                if ind == 50:
                    lid_unit0.drain_node = "J04"

    Continuing on the previous example, either during the simulation or after
    it completes, the user has access to lid unit results.  The following code
    provides details on how to access differne LidUnit results

    .. code-block:: python

        from pyswmm import Simulation, LidGroups

        with Simulation('lid_model.inp') as sim:
            # This returns an LidGroup object
            lid_group_j1_j3 = LidGroups(sim)["J1_J3_qqqqqqq"]

            # Next to get access to one of the LID units
            # inside this subcatchment it is indexed.

            # This returns an LidUnit object
            lid_unit0=lid_group_j1_j3[0]

            for ind, step in enumerate(sim):
                if ind == 50:
                    lid_unit0.drain_node = "J04"

            surface = lid_unit0.surface
            pavement = lid_unit0.pavement
            soil = lid_unit0.soil
            storage = lid_unit0.storage
            water_balance = lid_unit0.water_balance
            print(water_balance.inflow)
            print(water_balance.evaporation)
            print(water_balance.infiltration)
            print(water_balance.surface_flow)
            print(water_balance.drain_flow)
            print(water_balance.initial_volume)
            print(water_balance.final_volume)
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model
        self._cuindex = 0
        self._nLidGroups = self._model.getProjectSize(
            ObjectType.SUBCATCH.value)

    def __len__(self):
        """
        Return number of defined LidGroups.
        Note that there are one lidgroup per subcatchment
        Use the expression 'len(LidGroups)'.

        :return: Number of LidGroups
        :rtype: int

        """
        return self._model.getProjectSize(ObjectType.SUBCATCH.value)

    def __contains__(self, subcatchmentid):
        """
        Checks if Subcatchment ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return self._model.ObjectIDexist(
            ObjectType.SUBCATCH.value, subcatchmentid)

    def __getitem__(self, subcatchmentid):
        if self.__contains__(subcatchmentid):
            return LidGroup(self._model, subcatchmentid)
        else:
            raise PYSWMMException("Subcatchment ID Does not Exist")

    def __iter__(self):
        return self

    def __next__(self):
        if self._cuindex < self._nLidGroups:
            lidgroupobject = self.__getitem__(self._subcatchmentid)
            self._cuindex += 1  # Next Iteration
            return lidgroupobject
        else:
            raise StopIteration()

    @property
    def _subcatchmentid(self):
        """Subcatchment ID."""
        return self._model.getObjectId(
            ObjectType.SUBCATCH.value, self._cuindex)


class LidGroup(object):
    """
    Methods and properties associated with a group of LIDs defined on a subcatchment

    :param object model: Open Model Instance
    :param str subcatchmentid: Name of subcatchment associated with the Lid Group
    """

    def __init__(self, model, subcatchmentid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if subcatchmentid not in model.getObjectIDList(
                ObjectType.SUBCATCH.value):
            raise PYSWMMException("Subcatchment ID Does not Exist")
        self._model = model
        self._subcatchmentid = subcatchmentid
        self._cuindex = 0
        self._nLidUnits = model.getLidUCount(subcatchmentid)

    def __str__(self):
        return self._subcatchmentid

    def __len__(self):
        """
        Return number of defined LidUnit per LidGroup.
        Note that there can be multiple LidUnit per subcatchment
        Use the expression 'len(LidGroup)'.

        :return: Number of LidUnit
        :rtype: int

        """
        return self._nLidUnits

    def __contains__(self, index):
        """
        Checks if Subcatchment ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return index < self._nLidUnits

    def __getitem__(self, index):
        if self.__contains__(index):
            return LidUnit(self._model, self._subcatchmentid, index)
        else:
            raise PYSWMMException("Lid Unit Does Not Exist")

    def __iter__(self):
        return self

    def __next__(self):
        if self._cuindex < self._nLidUnits:
            lidunitobject = self.__getitem__(self._cuindex)
            self._cuindex += 1  # Next Iteration
            return lidunitobject
        else:
            raise StopIteration()

    @property
    def pervious_area(self):
        """
        Get lid group amount of pervious area

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidGResult(self._subcatchmentid,
                                         LidResults.pervArea.value)

    @property
    def flow_to_pervious(self):
        """
        Get lid group total flow sent to pervious area

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidGResult(self._subcatchmentid,
                                         LidResults.flowToPerv.value)

    @property
    def old_drain_flow(self):
        """
        Get lid group total drain flow in pervious period

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidGResult(self._subcatchmentid,
                                         LidResults.oldDrainFlow.value)

    @property
    def new_drain_flow(self):
        """
        Get lid group total drain flow in current period

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidGResult(self._subcatchmentid,
                                         LidResults.newDrainFlow.value)


class LidUnit(object):
    """
    Lid Unit Methods.

    :param object model: Open Model Instance
    :param str subcatchmentid: Subcatchment ID
    :param str lidid: Lid unit ID

    Lid Unit Parameters

    +--------------------+--------------------+--------------------+--------------------+
    | Parameter          | Getter             | Setter Before Sim  | Setter During Sim  |
    +====================+====================+====================+====================+
    | subcatchment       | enabled            | disabled           | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | lid_control        | enabled            | disabled           | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | unit_area          | enabled            | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | full_width         | enabled            | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | initial_saturation | enabled            | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | from_impervious    | enabled            | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | from_pervious      | enabled            | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | index              | enabled            | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | number             | enabled            | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | to_pervious        | enabled            | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | drain_subcatchment | enabled            | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    | drain_node         | enabled            | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    """

    def __init__(self, model, subcatchmentid, lidid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model
        self._subcatchmentid = subcatchmentid
        self._lidid = lidid

        self.surface = Surface(model, self)
        self.pavement = Pavement(model, self)
        self.soil = Soil(model, self)
        self.storage = Storage(model, self)
        self.water_balance = WaterBalance(model, self)

    @property
    def subcatchment(self):
        return self._subcatchmentid

    @property
    def lid_control(self):
        index = self.index
        return self._model.getObjectId(ObjectType.LID.value,
                                       index)

    @property
    def unit_area(self):
        """
        Get lid unit area.

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.unitArea.value)

    @unit_area.setter
    def unit_area(self, param):
        """Set lid unit area"""
        return self._model.setLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.unitArea.value,
                                        param)

    @property
    def full_width(self):
        """
        Get lid unit full top width.

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.fullWidth.value)

    @full_width.setter
    def full_width(self, param):
        """Set lid unit full top width."""
        return self._model.setLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.fullWidth.value,
                                        param)

    @property
    def initial_saturation(self):
        """
        Get lid initial saturation of soil and storage layers.

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.initSat.value)

    @initial_saturation.setter
    def initial_saturation(self, param):
        """Set lid initial saturation of soil and storage layers."""
        return self._model.setLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.initSat.value,
                                        param)

    @property
    def from_impervious(self):
        """
        Get lid fraction of impervious area runoff treated

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.fromImperv.value)

    @from_impervious.setter
    def from_impervious(self, param):
        """Set lid fraction of impervious area runoff treated"""
        return self._model.setLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.fromImperv.value,
                                        param)

    @property
    def from_pervious(self):
        """
        Get lid fraction of pervious area runoff treated

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.fromPerv.value)

    @ from_pervious.setter
    def from_pervious(self, param):
        """Set lid fraction of pervious area runoff treated"""
        return self._model.setLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.fromPerv.value,
                                        param)

    @property
    def index(self):
        """
        Get lid control index

        :return: Parameter Value
        :rtype: int
        """
        return self._model.getLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.index.value)

    @index.setter
    def index(self, param):
        """Set lid control index """
        if isinstance(param, str) and self._model.ObjectIDexist(
                ObjectType.LID.value, param):
            controlIndex = self._model.getObjectIDIndex(
                ObjectType.LID.value, param)
        elif isinstance(param, int) and param >= 0 and param < self._model.getProjectSize(ObjectType.LID.value):
            controlIndex = param
        else:
            controlIndex = 0
            raise PYSWMMException("Invalid Input")

        return self._model.setLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.index.value,
                                         controlIndex)

    @property
    def number(self):
        """
        Get lid number of replicate units

        :return: Parameter Value
        :rtype: int
        """
        return self._model.getLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.number.value)

    @number.setter
    def number(self, param):
        """Set lid number of replicate units"""
        return self._model.setLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.number.value,
                                         param)

    @property
    def to_pervious(self):
        """
        Get lid to pervious area (1 if outflow sent to pervious area)
                                 (0 if not)

        :return: Parameter Value
        :rtype: int
        """
        return self._model.getLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.toPerv.value)

    @to_pervious.setter
    def to_pervious(self, param):
        """
        Set lid to pervious area (1 if outflow sent to pervious area)
                                 (0 if not)
        """
        return self._model.setLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.toPerv.value,
                                         param)

    @property
    def drain_subcatchment(self):
        """
        Get lid drain to subcatchment index
        Negative if no recieving subcatchment

        :return: Parameter Value
        :rtype: int
        """
        return self._model.getLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.drainSub.value)

    @drain_subcatchment.setter
    def drain_subcatchment(self, param):
        """Set lid drain to subcatchment index"""
        if isinstance(param, str) and self._model.ObjectIDexist(
                ObjectType.SUBCATCH.value, param):
            subIndex = self._model.getObjectIDIndex(
                ObjectType.SUBCATCH.value, param)
        elif isinstance(param, int) and param >= -1 and param < self._model.getProjectSize(ObjectType.SUBCATCH.value):
            subIndex = param
        else:
            subIndex = 0
            raise PYSWMMException("Invalid Input")

        self._model.setLidUOption(self._subcatchmentid,
                                  self._lidid,
                                  LidUOptions.drainSub.value,
                                  subIndex)

    @property
    def drain_node(self):
        """
        Get lid drain to node index
        Negative if no recieving node

        :return: Parameter Value
        :rtype: int
        """
        return self._model.getLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.drainNode.value)

    @drain_node.setter
    def drain_node(self, param):
        """Set lid drain to node index"""
        if isinstance(param, str) and self._model.ObjectIDexist(
                ObjectType.NODE.value, param):
            nodeIndex = self._model.getObjectIDIndex(
                ObjectType.NODE.value, param)
        elif isinstance(param, int) and param >= -1 and param < self._model.getProjectSize(ObjectType.NODE.value):
            nodeIndex = param
        else:
            nodeIndex = 0
            raise PYSWMMException("Invalid Input")

        self._model.setLidUOption(self._subcatchmentid,
                                  self._lidid,
                                  LidUOptions.drainNode.value,
                                  nodeIndex)

    @property
    def dry_time(self):
        """
        Get lid time since last rainfall (sec)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.dryTime.value)

    @property
    def old_drain_flow(self):
        """
        Get lid pervious drain flow

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.oldDrainFlow.value)

    @property
    def new_drain_flow(self):
        """
        Get lid current drain flow

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.newDrainFlow.value)

    @property
    def evaporation(self):
        """
        Get lid current evaporation rate

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.evapRate.value)

    @property
    def native_infiltration(self):
        """
        Get lid native infilration rate limit

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.nativeInfil.value)
