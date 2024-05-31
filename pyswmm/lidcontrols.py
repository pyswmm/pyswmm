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
    """Lid Control Iterator Methods.

    :param object model: Open Model Instance

    This allows the user to iterate and get on of the LID control types as
    defined inside SWMM's [LID_CONTROLS] section.  For example, here is a sample
    section from a SWMM INP file.

    .. code-block::

        [LID_CONTROLS]
        ;;Name           Type_Layer Parameters
        ;;-------------- ---------- ----------
        LID_C1  IT
        LID_C1  SURFACE    0.0    0.0    0.03   1.0    5
        LID_C1  STORAGE    800    0.3    3.6    0      NO
        LID_C1  DRAIN      0.5    1.41   400    6      0       0

    Now we can peform manipulations in PySWMM and get objects.

    .. code-block:: python

        from pyswmm import Simulation, LidControls

        with Simulation('lid_model.inp') as sim:
            for lid_control in LidControls(sim):
                print(lid_control)

    .. code-block::

        >>> LID_C1
        >>> lid_control_type_2

    It is also possible to simply get an LID control by name as follows:

    .. code-block:: python

        from pyswmm import Simulation, LidControls

        with Simulation('lid_model.inp') as sim:
            lid_control = LidControls(sim)['LID_C1']
            print(lid_control)

    .. code-block::

        >>> LID_C1

    Once the LID control object is instantiated, there are getter and setters
    available for each different layer of the LID Control.  The layers are the
    following and these become instance attributes of each LID Control (LidControl)
    object.

    +------------+-----------+
    | Layer Type | Attribute |
    +============+===========+
    | Surface    | surface   |
    +------------+-----------+
    | Soil       | soil      |
    +------------+-----------+
    | Storage    | storage   |
    +------------+-----------+
    | Pavement   | pavement  |
    +------------+-----------+
    | Drain      | drain     |
    +------------+-----------+
    | DrainMat   | drain_mat |
    +------------+-----------+

    In our example model section above the layers defined are Surface,
    Storage, and Drain.  Once the handles are available, the properties
    and setter methods can be called to read and modify the values.

    .. code-block:: python

        from pyswmm import Simulation, LidControls

        with Simulation('lid_model.inp') as sim:
            lid_control = LidControls(sim)['LID_C1']

            # Handles to get/set params for each layer
            lid_control_surface = lid_control.surface
            lid_control_storage = lid_control.storage
            lid_control_drain = lid_control.drain

            print(lid_control_surface.roughness)
            lid_control_surface.roughness = 0.5
            print(lid_control_surface.roughness)

            for step in sim:
                pass

    .. code-block::

        >>> 0.03
        >>> 0.5

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
        return self._model.ObjectIDexist(ObjectType.LID.value, lidcontrolid)

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
        return self._model.getObjectId(ObjectType.LID.value, self._cuindex)


class LidControl(object):
    """
    Once the LID control object is instantiated, there are getter and setters
    available for each different layer of the LID Control.  The layers are the
    following and these become instance attributes of each LID Control (LidControl)
    object.

    +------------+-----------+
    | Layer Type | Attribute |
    +============+===========+
    | Surface    | surface   |
    +------------+-----------+
    | Soil       | soil      |
    +------------+-----------+
    | Storage    | storage   |
    +------------+-----------+
    | Pavement   | pavement  |
    +------------+-----------+
    | Drain      | drain     |
    +------------+-----------+
    | DrainMat   | drain_mat |
    +------------+-----------+
    """

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
