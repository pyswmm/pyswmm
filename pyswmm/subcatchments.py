 # -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Subcatchments module for the pythonic interface to SWMM5."""

# Local imports
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import ObjectType, SubcParams, SubcPollut, SubcResults


class Subcatchments(object):
    """
    Subcatchment Iterator Methods.

    :param object model: Open Model Instance

    Examples:

    >>> from pyswmm import Simulation, Subcatchments
    >>>
    >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
    ...     for subcatchment in Subcatchments(sim):
    ...         print(subcatchment)
    ...         print(subcatchment.subcatchmentid)
    <swmm5.Subcatchment object at 0x031B0350>
    S1
    <swmm5.Subcatchment object at 0x030693D0>
    S2
    <swmm5.Subcatchment object at 0x031B0350>
    S3
    <swmm5.Subcatchment object at 0x030693D0>
    S4

    Iterating over Subcatchments Object

    >>> subcatchments = Subcatchments(sim)
    >>> for subcatchment in subcatchments:
    ...     print(subcatchment.subcatchmentid)
    S0
    S1
    S2
    S3

    Testing Existence

    >>> subcatchments = Subcatchments(sim)
    >>> "S1" in subcatchments
    True

    Initializing a subcatchment Object

    >>> subcatchments = Subcatchments(sim)
    >>> s1 = subcatchments['S1']
    >>> print(s1.area)
    12
    >>>
    >>> s1.area = 200
    >>> print(s1.area)
    200
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model
        self._cuindex = 0
        self._nSubcatchments = self._model.getProjectSize(
            ObjectType.SUBCATCH.value)

    def __len__(self):
        """
        Return number of subcatchments.

        Use the expression 'len(Subcatchments)'.

        :return: Number of Subcatchments
        :rtype: int

        """
        return self._model.getProjectSize(ObjectType.SUBCATCH.value)

    def __contains__(self, subcatchmentid):
        """
        Checks if Subcatchment ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return self._model.ObjectIDexist(ObjectType.SUBCATCH.value,
                                         subcatchmentid)

    def __getitem__(self, subcatchmentid):
        if self.__contains__(subcatchmentid):
            return Subcatchment(self._model, subcatchmentid)
        else:
            raise PYSWMMException("Subcatchment ID Does not Exist")

    def __iter__(self):
        return self

    def __next__(self):
        if self._cuindex < self._nSubcatchments:
            subcatchmentobject = self.__getitem__(self._subcatchmentid)
            self._cuindex += 1  # Next Iteration
            return subcatchmentobject
        else:
            raise StopIteration()

    @property
    def _subcatchmentid(self):
        """Subcatchment ID."""
        return self._model.getObjectId(ObjectType.SUBCATCH.value,
                                       self._cuindex)


class Subcatchment(object):
    """
    Subcatchment Methods.

    :param object model: Open Model Instance
    :param str subcatchmentid: Subcatchment ID

    Examples:

    >>> from pyswm import Simulation, Subcatchments
    >>>
    >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
    ...     s1 = Subcatchments(sim)["S1"]
    ...     print(s1.rainfall)
    ...     for step in sim:
    ...         print(s1.rainfall)
    0.04
    """

    def __init__(self, model, subcatchmentid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if subcatchmentid not in model.getObjectIDList(
                ObjectType.SUBCATCH.value):
            raise PYSWMMException("ID Not valid")
        self._model = model
        self._subcatchmentid = subcatchmentid

    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def subcatchmentid(self):
        """
        Get Subcatchment ID.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.subcatchmentid)
        S1
        """
        return self._subcatchmentid

    @property
    def connection(self):
        """
        Get Subcatchment Outlet Connection.

        This function return the type of loading surface and the ID. The two
        load to objects are nodes and other subcatchments.

        +--------------+---+
        | Node         | 2 |
        +--------------+---+
        | Subcatchment | 1 |
        +--------------+---+

        :return: (Loading Surface Type, ID)
        :rtype: tuple

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.connection)
        (2, 'J2')
        """
        return self._model.getSubcatchOutConnection(self._subcatchmentid)

    @property
    def width(self):
        """
        Get/set subcatchment width.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.width)
        100.0

        Setting the value

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.width)
        ...     s1.width = 30
        ...     print(s1.width)
        100
        30
        """
        return self._model.getSubcatchParam(self._subcatchmentid,
                                            SubcParams.width.value)

    @width.setter
    def width(self, param):
        """Set Subcatchment Width."""
        self._model.setSubcatchParam(self._subcatchmentid,
                                     SubcParams.width.value, param)

    @property
    def area(self):
        """
        Get/set subcatchment area.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.area)
        10

        Setting the value

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.area)
        ...     s1.area = 50
        ...     print(s1.area)
        10
        50
        """
        return self._model.getSubcatchParam(self._subcatchmentid,
                                            SubcParams.area.value)

    @area.setter
    def area(self, param):
        """Set Subcatchment area."""
        self._model.setSubcatchParam(self._subcatchmentid,
                                     SubcParams.area.value, param)

    @property
    def percent_impervious(self):
        """
        Get/set subcatchment percent impervious.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.percent_impervious)
        10

        Setting the value

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.percent_impervious)
        ...     s1.percent_impervious = 50
        ...     print(s1.percent_impervious)
        10
        50
        """
        return self._model.getSubcatchParam(self._subcatchmentid,
                                            SubcParams.fracImperv.value)

    @percent_impervious.setter
    def percent_impervious(self, param):
        """Set Subcatchment percent impervious."""
        self._model.setSubcatchParam(self._subcatchmentid,
                                     SubcParams.fracImperv.value, param)

    @property
    def slope(self):
        """
        Get/set subcatchment slope.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.slope)
        0.01

        Setting the value

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.slope)
        ...     s1.slope = 0.02
        ...     print(s1.slope)
        0.1
        0.2
        """
        return self._model.getSubcatchParam(self._subcatchmentid,
                                            SubcParams.slope.value)

    @slope.setter
    def slope(self, param):
        """Set Subcatchment Ponding Area."""
        self._model.setSubcatchParam(self._subcatchmentid,
                                     SubcParams.slope.value, param)

    @property
    def curb_length(self):
        """
        Get/set subcatchment curb length.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.curb_length)
        0

        Setting the value

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     print(s1.curb_length)
        ...     s1.curb_length = 100
        ...     print(s1.curb_length)
        0
        100
        """
        return self._model.getSubcatchParam(self._subcatchmentid,
                                            SubcParams.curbLength.value)

    @curb_length.setter
    def curb_length(self, param):
        """Set Subcatchment curb length."""
        self._model.setSubcatchParam(self._subcatchmentid,
                                     SubcParams.curbLength.value, param)

    @property
    def rainfall(self):
        """
        Get Subcatchment Results for Rainfall.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     for step in sim:
        ...         print(s1.rainfall)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getSubcatchResult(self._subcatchmentid,
                                             SubcResults.rainfall.value)

    @property
    def evaporation_loss(self):
        """
        Get Subcatchment Results for evaporation loss.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     for step in sim:
        ...         print(s1.evaporation_loss)
        0.01
        0.01
        0.01
        0.01
        0.01
        """
        return self._model.getSubcatchResult(self._subcatchmentid,
                                             SubcResults.evapLoss.value)

    @property
    def infiltration_loss(self):
        """
        Get Subcatchment Results for Infiltration Loss.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     for step in sim:
        ...         print(s1.infiltration_loss)
        0
        0.01
        0.01
        0.01
        0.01
        """
        return self._model.getSubcatchResult(self._subcatchmentid,
                                             SubcResults.infilLoss.value)

    @property
    def runon(self):
        """
        Get Subcatchment Results for Run On.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     for step in sim:
        ...         print(s1.runon)
        0
        1.2
        1.5
        1.9
        1.2
        """
        return self._model.getSubcatchResult(self._subcatchmentid,
                                             SubcResults.runon.value)

    @property
    def runoff(self):
        """
        Get Subcatchment Results for Run Off Rate.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     for step in sim:
        ...         print(s1.runoff)
        0
        0
        0.01
        0
        0
        """
        return self._model.getSubcatchResult(self._subcatchmentid,
                                             SubcResults.newRunoff.value)

    @property
    def snow_depth(self):
        """
        Get Subcatchment Results for Snow Depth.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     for step in sim:
        ...         print(s1.snow_depth)
        0
        0.5
        0.51
        0.52
        0.49
        """
        return self._model.getSubcatchResult(self._subcatchmentid,
                                             SubcResults.newSnowDepth.value)

    @property
    def buildup(self):
        """
        Get Pollutant Results for Surface Buildup on a Subcatchment.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Group of Subcatchment Surface Buildup Values.
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/buildup-test.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     for step in sim:
        ...         print(s1.buildup)
        {'test-pollutant': 8.0}
        {'test-pollutant': 8.0}
        {'test-pollutant': 7.998}
        {'test-pollutant': 7.991}
        {'test-pollutant': 7.981}
        """
        out_dict = {}
        pollut_ids = self._model.getObjectIDList(ObjectType.POLLUT.value)
        buildup_array = self._model.getSubcatchPollut(self._subcatchmentid,
                                                      SubcPollut.buildup.value)

        for ind in range(len(pollut_ids)):
            out_dict[pollut_ids[ind]] = buildup_array[ind]

        return out_dict

    @property
    def conc_ponded(self):
        """
        Get Pollutant Results for Current Concentration of Pollutant in Ponded
        Water on a Subcatchment.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Group of Subcatchment Ponded Water Quality Values.
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/buildup-test.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     for step in sim:
        ...         print(s1.conc_ponded)
        {'test-pollut1': 0.0, 'test-pollut2': 0.0}
        {'test-pollut1': 0.0, 'test-pollut2': 0.0}
        {'test-pollut1': 0.0, 'test-pollut2': 0.0}
        """
        out_dict = {}
        pollut_ids = self._model.getObjectIDList(ObjectType.POLLUT.value)
        cPonded_array = self._model.getSubcatchPollut(
            self._subcatchmentid, SubcPollut.concPonded.value)
        for ind in range(len(pollut_ids)):
            out_dict[pollut_ids[ind]] = cPonded_array[ind]

        return out_dict

    @property
    def pollut_quality(self):
        """
        Get Current Pollutant Water Quality Results from Subcatchment Runoff.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Group of Subcatchment Runoff Pollutant Quality Values.
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/buildup-test.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     for step in sim:
        ...         print(s1.pollut_quality)
        {'TSS': 0.0, 'Lead': 0.0}
        {'TSS': 0.0, 'Lead': 0.0}
        {'TSS': 0.0, 'Lead': 0.0}
        """
        out_dict = {}
        pollut_ids = self._model.getObjectIDList(ObjectType.POLLUT.value)
        subcqual_array = self._model.getSubcatchPollut(self._subcatchmentid,
                                                      SubcPollut.subcQual.value)

        for ind in range(len(pollut_ids)):
            out_dict[pollut_ids[ind]] = subcqual_array[ind]

        return out_dict
        
    @property
    def runoff_total_loading(self):
        """
        Get Total Pollutant Loading from Subcatchment Runoff.

        If Simulation is not running this method will raise a warning and
        return 0.

        :return: Group of Subcatchment Runoff Pollutant Loading Values.
        :rtype: dict

        Examples:

        >>> from pyswmm import Simulation, Subcatchments
        >>>
        >>> with Simulation('tests/buildup-test.inp') as sim:
        ...     s1 = Subcatchments(sim)["S1"]
        ...     for step in sim:
        ...         print(s1.runoff_total_loading)
        {'TSS': 0.01, 'Lead': 0.001}
        {'TSS': 0.02, 'Lead': 0.002}
        {'TSS': 0.03, 'Lead': 0.003}
        """
        out_dict = {}
        pollut_ids = self._model.getObjectIDList(ObjectType.POLLUT.value)
        totalload_array = self._model.getSubcatchPollut(self._subcatchmentid,
                                                      SubcPollut.subcTotalLoad.value)

        for ind in range(len(pollut_ids)):
            out_dict[pollut_ids[ind]] = totalload_array[ind]

        return out_dict

    @property
    def statistics(self):
        """
        Subcatchment Flow Stats. The stats returned are rolling/cumulative.
        Indeces are as follows:

        +-------------------+
        | precipitation     |
        +-------------------+
        | runon             |
        +-------------------+
        | evaporation       |
        +-------------------+
        | infiltration      |
        +-------------------+
        | runoff            |
        +-------------------+
        | peak_runoff_rate  |
        +-------------------+

        :return: Group of Stats
        :rtype: dict
        """
        return self._model.subcatch_statistics(self.subcatchmentid)
