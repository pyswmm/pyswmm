# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Base class for a SWMM Simulation."""

# Local imports
from pyswmm.swmm5 import PySWMM, PYSWMMException
from pyswmm.toolkitapi import SimulationTime, SimulationUnits


class Simulation(object):
    """
    Base class for a SWMM Simulation.

    The model object provides several options to run a simulation.

    Examples:

    Intialize a simulation and iterate through a simulation. This
    approach requires some clean up.

    >>> from pyswmm import Simulation
    >>>
    >>> sim = Simulation('./TestModel1_weirSetting.inp')
    >>> for step in sim:
    ...     pass
    >>>
    >>> sim.report()
    >>> sim.close()

    Intialize using with statement.  This automatically cleans up
    after a simulation

    >>> from pyswmm import Simulation
    >>>
    >>> with Simulation('./TestModel1_weirSetting.inp') as sim:
    ...     for step in sim:
    ...         pass
    ...     sim.report()

    Initialize the simulation and execute. This style does not allow
    the user to interact with the simulation. However, this approach
    tends to be the fastest.

    >>> from pyswmm import Simulation
    >>>
    >>> sim = Simulation('./TestModel1_weirSetting.inp')
    >>> sim.execute()
    """

    def __init__(self, inputfile, reportfile=None, outputfile=None):
        self._model = PySWMM(inputfile, reportfile, outputfile)
        self._model.swmm_open()
        self._isOpen = True
        self._advance_seconds = None
        self._isStarted = False
        self._initial_conditions = None

    def __enter__(self):
        """
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     for step in sim:
        ...         print(sim.current_time)
        ...     sim.report()
        >>>
        >>> 2015-11-01 14:00:30
        >>> 2015-11-01 14:01:00
        >>> 2015-11-01 14:01:30
        >>> 2015-11-01 14:02:00
        """
        return self

    def __iter__(self):
        """Iterator over Simulation"""
        return self

    def start(self):
        """Start Simulation"""
        if not self._isStarted:
            # Set Model Initial Conditions
            if self._initial_conditions:
                self._initial_conditions()
            self._model.swmm_start(True)
            self._isStarted = True

    def __next__(self):
        """Next"""
        # Start Simulation
        self.start()

        # Simulation Step Amount
        if self._advance_seconds is None:
            time = self._model.swmm_step()
        else:
            time = self._model.swmm_stride(self._advance_seconds)

        if time <= 0.0:
            self._model.swmm_end()
            self._isStarted = False
            raise StopIteration
        return self._model

    next = __next__  # Python 2

    def __exit__(self, *a):
        """close"""
        if self._isStarted:
            self._model.swmm_end()
            self._isStarted = False
        if self._isOpen:
            self._model.swmm_close()
            self._isOpen = False

    def initial_conditions(self, init_conditions):
        """
        Intial Conditions for Hydraulics and Hydrology can be set
        from within the api by setting a function to the
        initial_conditions property.

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('./TestModel1_weirSetting.inp') as sim:
        ...     nodeJ1 = Nodes(sim)["J1"]
        ...
        ...     def init_conditions():
        ...         nodeJ1.initial_depth = 4
        ...
        ...     sim.initial_conditions(init_conditions)
        ...
        ...     for step in sim:
        ...         pass
        ...     sim.report()

        """
        if hasattr(init_conditions, '__call__'):
            self._initial_conditions = init_conditions
        else:
            error_msg = 'Requires Type Function, not {}'.format(
                type(init_conditions))
            raise (PYSWMMException(error_msg))

    def step_advance(self, advance_seconds):
        """
        Advances the model by X number of seconds instead of
        intervening at every routing step.  This does not change
        the routing step for the simulation; only lets python take
        back control after each advance period.

        :param int advance_seconds: Seconds to Advance simulation

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     sim.step_advance(300)
        ...     for step in sim:
        ...         print(step.current_time)
        ...         # or here! sim.step_advance(newvalue)
        ...     sim.report()
        >>>
        >>> 2015-11-01 14:00:30
        >>> 2015-11-01 14:01:00
        >>> 2015-11-01 14:01:30
        >>> 2015-11-01 14:02:00
        """
        self._advance_seconds = advance_seconds

    def report(self):
        """
        Writes to report file after simulation.

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     for step in sim:
        ...         pass
        ...     sim.report()
        """
        self._model.swmm_report()

    def close(self):
        """
        Intialize a simulation and iterate through a simulation. This
        approach requires some clean up.

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> sim = Simulation('./TestModel1_weirSetting.inp')
        >>> for step in sim:
        ...     pass
        >>>
        >>> sim.report()
        >>> sim.close()
        """
        self.__exit__()

    def execute(self):
        """
        Open an input file, run SWMM, then close the file.

        Examples:

        >>> sim = PYSWMM(r'\\test.inp')
        >>> sim.execute()
        """
        self._model.swmmExec()

    @property
    def engine_version(self):
        """
        Retrieves the SWMM Engine Version.

        :return: Engine Version
        :rtype: StrictVersion

        Examples:

        >>> sim = PYSWMM(r'\\test.inp')
        >>> sim.engine_version
        StrictVersion("5.1.13")
        """
        return self._model.swmm_getVersion()

    @property
    def runoff_error(self):
        """
        Retrieves the Runoff Mass Balance Error.

        :return: Runoff Mass Balance Error
        :rtype: float

        Examples:

        >>> sim = PYSWMM(r'\\test.inp')
        >>> sim.execute()
        >>> sim.runoff_error
        0.01
        """
        return self._model.swmm_getMassBalErr()[0]

    @property
    def flow_routing_error(self):
        """
        Retrieves the Flow Routing Mass Balance Error.

        :return: Flow Routing Mass Balance Error
        :rtype: float

        Examples:

        >>> sim = PYSWMM(r'\\test.inp')
        >>> sim.execute()
        >>> sim.flow_routing_error
        0.01
        """
        return self._model.swmm_getMassBalErr()[1]

    @property
    def quality_error(self):
        """
        Retrieves the Quality Routing Mass Balance Error.

        :return: Quality Routing Mass Balance Error
        :rtype: float

        Examples:

        >>> sim = PYSWMM(r'\\test.inp')
        >>> sim.execute()
        >>> sim.quality_error
        0.01
        """
        return self._model.swmm_getMassBalErr()[2]

    @property
    def start_time(self):
        """Get/set Simulation start time.

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     print sim.start_time
        ...     sim.start_time = datetime(2015,5,10,15,15,1)
        >>>
        >>> datetime.datetime(2015,5,10,15,15,1)
        """
        return self._model.getSimulationDateTime(
            SimulationTime.StartDateTime.value)

    @start_time.setter
    def start_time(self, dtimeval):
        """Set simulation Start time"""
        self._model.setSimulationDateTime(SimulationTime.StartDateTime.value,
                                          dtimeval)

    @property
    def end_time(self):
        """Get/set Simulation end time.

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     print sim.end_time
        ...     sim.end_time = datetime(2016,5,10,15,15,1)
        >>>
        >>> datetime.datetime(2016,5,10,15,15,1)
        """
        return self._model.getSimulationDateTime(
            SimulationTime.EndDateTime.value)

    @end_time.setter
    def end_time(self, dtimeval):
        """Set simulation End time."""
        self._model.setSimulationDateTime(SimulationTime.EndDateTime.value,
                                          dtimeval)

    @property
    def report_start(self):
        """Get/set Simulation report start time.

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     print sim.report_start
        ...     sim.report_start = datetime(2015,5,10,15,15,1)
        >>>
        >>> datetime.datetime(2015,5,10,15,15,1)
        """
        return self._model.getSimulationDateTime(
            SimulationTime.ReportStart.value)

    @report_start.setter
    def report_start(self, dtimeval):
        """Set simulation report start time."""
        self._model.setSimulationDateTime(SimulationTime.ReportStart.value,
                                          dtimeval)

    @property
    def flow_units(self):
        """
        Get Simulation Units (CFS, GPM, MGD, CMS, LPS, MLD).

        :return: Flow Unit
        :rtype: str

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     print sim.flow_units
        >>>
        >>> CFS
        """
        return self._model.getSimUnit(SimulationUnits.FlowUnits.value)

    @property
    def system_units(self):
        """Get system units (US, SI).

        :return: System Unit
        :rtype: str

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     print sim.system_units
        >>>
        >>> US
        """
        return self._model.getSimUnit(SimulationUnits.UnitSystem.value)

    @property
    def current_time(self):
        """Get Simulation Current Time.

        :return: Current Simulation Time
        :rtype: Datetime

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     for step in sim:
        ...         print(sim.current_time)
        ...     sim.report()
        >>>
        >>> 2015-11-01 14:00:30
        >>> 2015-11-01 14:01:00
        >>> 2015-11-01 14:01:30
        >>> 2015-11-01 14:02:00
        """
        return self._model.getCurrentSimulationTime()

    @property
    def percent_complete(self):
        """Get Simulation Percent Complete.

        :return: Current Percent Complete
        :rtype: Datetime

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     for step in sim:
        ...         print(sim.percent_complete)
        ...     sim.report()
        >>>
        >>> 0.01
        >>> 0.25
        >>> 0.50
        >>> 0.75
        """
        dt = self.current_time - self.start_time
        total_time = self.end_time - self.start_time
        return float(dt.total_seconds()) / total_time.total_seconds()
