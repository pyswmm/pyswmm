# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2019 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Raingages module for the pythonic interface to SWMM5."""

# Local imports
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import RainGageResults, ObjectType


class RainGages(object):
    """
    Rain Gages Iterator Methods.

    :param object model: Open Model Instance

    Examples:

    >>> from pyswmm import Simulation, Nodes
    >>>
    >>> with Simulation('tests/data/TestModel1_weirSetting.inp') as sim:
    ...     for raingage in RainGages(sim):
    ...         print(raingage)
    ...         print(raingage.raingageid)
    ...
    >>> <swmm5.RainGage object at 0x031B0350>
    >>> Gage1
    >>> <swmm5.RainGage object at 0x030693D0>
    >>> Gage4
    >>> <swmm5.RainGage object at 0x031B0350>
    >>> Gage3
    >>> <swmm5.RainGage object at 0x030693D0>
    >>> Gage10

    Iterating over Nodes Object

    >>> raingages = RainGages(sim)
    >>> for raingage in raingages:
    ...     print(raingage.raingageid)
    >>> Gage1
    >>> Gage4
    >>> Gage3
    >>> Gage10

    Testing Existence

    >>> raingages = RainGages(sim)
    >>> "Gage1" in raingages
    >>> True

    Initializing a node Object

    >>> raingages = RainGages(sim)
    >>> gage1 = raingages['Gage1']
    >>> print(gage1.total_precip)
    >>> 0.04
    >>>
    >>> gage1.total_precip = 1
    >>> print(gage1.total_precip)
    >>> 1
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model
        self._cuindex = 0
        self._nRaingages = self._model.getProjectSize(ObjectType.GAGE.value)

    def __len__(self):
        """
        Return number of raingages. Use the expression 'len(RainGages(sim))'.

        :return: Number of Raingages
        :rtype: int

        """
        return self._model.getProjectSize(ObjectType.GAGE.value)

    def __contains__(self, raingageid):
        """
        Checks if Rain Gage ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return self._model.ObjectIDexist(ObjectType.GAGE.value, raingageid)

    def __getitem__(self, raingageid):
        if self.__contains__(raingageid):
            rg = RainGage(self._model, raingageid)
            return rg
        else:
            raise PYSWMMException(
                "Raingage ID: {} Does not Exist".format(raingageid))

    def __iter__(self):
        return self

    def __next__(self):
        if self._cuindex < self._nRaingages:
            raingageobject = self.__getitem__(self._raingageid)
            self._cuindex += 1  # Next Iteration
            return raingageobject
        else:
            raise StopIteration()

    @property
    def _raingageid(self):
        """Node ID."""
        return self._model.getObjectId(ObjectType.GAGE.value, self._cuindex)


class RainGage(object):
    """
    Raingage Methods.

    :param object model: Open Model Instance
    :param str raingageid: Raingage ID

    Examples:

    >>> from pyswmm import Simulation, Raingages
    >>>
    >>> with Simulation('tests/data/TestModel1_weirSetting.inp') as sim:
    ...     rg1 = Raingages(sim)["Gage1"]
    ...     print(rg1.raingageid)
    ...     for step in sim:
    ...         print(rg1.total_precip)
    ... Gage1
    ... 0
    ... 10
    """

    def __init__(self, model, raingageid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if raingageid not in model.getObjectIDList(ObjectType.GAGE.value):
            raise PYSWMMException("ID Not valid")
        self._model = model
        self._raingageid = raingageid

    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def raingageid(self):
        """
        Get Rain Gage ID.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, RainGages
        >>>
        >>> with Simulation('tests/data/TestModel1_weirSetting.inp') as sim:
        ...     rg = RainGage(sim)["Gage1"]
        ...     print(rg.raingageid)
        >>> Gage1
        """
        return self._raingageid

    @property
    def total_precip(self):
        """
        Get/set raingage total precipitation rate (like in/hr or mm/hr).

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, RainGages
        >>>
        >>> with Simulation('tests/data/TestModel1_weirSetting.inp') as sim:
        ...     rg1 = RainGages(sim)["Gage1"]
        ...     print(rg1.total_precip)
        >>> 1.0

        Setting the value

        >>> from pyswmm import Simulation, RainGages
        >>>
        >>> with Simulation('tests/data/TestModel1_weirSetting.inp') as sim:
        ...     rg1 = RainGages(sim)["Gage1"]
        ...     print(rg1.total_precip)
        ...     rg1.total_precip = 0.2
        ...     print(rg1.total_precip)
        >>> 1.0
        >>> 0.2
        """
        return self._model.getGagePrecip(self._raingageid, RainGageResults.total_precip)

    @total_precip.setter
    def total_precip(self, param):
        """Set Total Precipitation Rate (in/hr or mm/hr)."""
        self._model.setGagePrecip(self._raingageid, param)

    @property
    def rainfall(self):
        """
        Get raingage total rainfall rate (like in/hr or mm/hr).

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, RainGages
        >>>
        >>> with Simulation('tests/data/TestModel1_weirSetting.inp') as sim:
        ...     rg1 = RainGages(sim)["Gage1"]
        ...     print(rg1.rainfall)
        >>> 1.0
        """
        return self._model.getGagePrecip(self._raingageid, RainGageResults.rainfall)

    @property
    def snowfall(self):
        """
        Get raingage total snowfall rate (like in/hr or mm/hr).

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, RainGages
        >>>
        >>> with Simulation('tests/data/TestModel1_weirSetting.inp') as sim:
        ...     rg1 = RainGages(sim)["Gage1"]
        ...     print(rg1.snowfall)
        >>> 0.0
        """
        return self._model.getGagePrecip(self._raingageid, RainGageResults.snowfall)
