# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2018 Jennifer Wu
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import ObjectType
from pyswmm.lidlayers import Surface, Soil, Storage, Pavement, Drain, DrainMat


class LidControls(object):
    """
    Lid Control Iterator Methods.

    :param object model: Open Model Instance
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._sim = model
        self._model = model._model
        self._cuindex = 0
        self._nlidcontrols = self._model.getProjectSize(ObjectType.LID.value)

    def __len__(self):
        """
        Return number of lid controls.

        Use the expression 'len(LidControls)'.

        :return: Number of Lid Controls
        :rtype: int

        """
        return self._model.getProjectSize(ObjectType.LID.value)

    def __contains__(self, lidcontrolid):
        """
        Checks if Lid Control ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return self._model.ObjectIDexist(ObjectType.LID.value,
                                         lidcontrolid)

    def __getitem__(self, lidcontrolid):
        if self.__contains__(lidcontrolid):
            return LidControl(self._sim, self._model, lidcontrolid)
        else:
            raise PYSWMMException("Lid Control ID Does not Exist")

    def __iter__(self):
        return self

    def __next__(self):
        if self._cuindex < self._nlidcontrols:
            lidcontrolobject = self.__getitem__(self._lidcontrolid)
            self._cuindex += 1  # Next Iteration
            return lidcontrolobject
        else:
            raise StopIteration()

    @property
    def _lidcontrolid(self):
        """Lid Control ID."""
        return self._model.getObjectId(ObjectType.LID.value,
                                       self._cuindex)


class LidControl(object):
    def __init__(self, sim, model, lidcontrolid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if lidcontrolid not in model.getObjectIDList(ObjectType.LID.value):
            raise PYSWMMException("ID Not valid")
        self._sim = sim
        self._model = model
        self._lidcontrolid = lidcontrolid

        self.surface = Surface(model, self)
        self.soil = Soil(model, self)
        self.storage = Storage(model, self)
        self.pavement = Pavement(model, self)
        self.drain = Drain(model, self)
        self.drain_mat = DrainMat(model, self)

    def __str__(self):
        return self._lidcontrolid

    @property
    def can_overflow(self):
        """
        Get lid control surface layer option for immediate outflow of excess water

        :return: Parameter Value
        :rtype: char
        """
        return self._model.getLidCOverflow(self._lidcontrolid)
