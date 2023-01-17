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
    User can specified SWMM library path. Uses default lib if not provided.

    Initialize the Simulation class.

    :param str inpfile: Name of SWMM input file (default '')
    :param str rptfile: Report file to generate (default None)
    :param str binfile: Optional binary output file (default None)
    :param str swmm_lib_path: User-specified SWMM library path (default None).

    Examples:

    Intialize a simulation and iterate through a simulation. This
    approach requires some clean up.

    >>> from pyswmm import Simulation
    >>>
    >>> sim = Simulation('tests/data/model_weir_setting.inp')
    >>> for step in sim:
    ...     pass
    >>>
    >>> sim.report()
    >>> sim.close()

    Intialize using with statement.  This automatically cleans up
    after a simulation

    >>> from pyswmm import Simulation
    >>>
    >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
    ...     for step in sim:
    ...         pass
    ...     sim.report()

    Initialize the simulation and execute. This style does not allow
    the user to interact with the simulation. However, this approach
    tends to be the fastest.

    >>> from pyswmm import Simulation
    >>>
    >>> sim = Simulation('tests/data/model_weir_setting.inp')
    >>> sim.execute()
    """

    def __init__(self,
                 inputfile,
                 reportfile=None,
                 outputfile=None,
                 swmm_lib_path=None):
        self._model = PySWMM(inputfile, reportfile, outputfile, swmm_lib_path)
        self._model.swmm_open()
        self._isOpen = True
        self._advance_seconds = None
        self._isStarted = False
        self._terminate_request = False
        self._callbacks = {
            "before_start": None,
            "before_step": None,
            "after_step": None,
            "before_end": None,
            "after_end": None,
            "after_close": None
        }

    def __enter__(self):
        """
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     for step in sim:
        ...         print(sim.current_time)
        ...     sim.report()
        2015-11-01 14:00:30
        2015-11-01 14:01:00
        2015-11-01 14:01:30
        2015-11-01 14:02:00
        """
        return self

    def __iter__(self):
        """Iterator over Simulation"""
        return self

    def start(self):
        """Start Simulation"""
        if not self._isStarted:
            # Set Model Initial Conditions
            # (This Will be Deprecated with Time)
            if hasattr(self, "_initial_conditions"):
                self._initial_conditions()
            # Execute Callback Hooks Before Simulation
            self._execute_callback(self.before_start())
            self._model.swmm_start(True)
            self._isStarted = True

    def __next__(self):
        """Next"""
        # Start Simulation
        self.start()
        # Check if simulation termination request was made
        if self._terminate_request:
            self._execute_callback(self.before_end())
            raise StopIteration
        # Execute Callback Hooks Before Simulation Step
        self._execute_callback(self.before_step())
        # Simulation Step Amount
        if self._advance_seconds is None:
            time = self._model.swmm_step()
        else:
            time = self._model.swmm_stride(self._advance_seconds)
        # Execute Callback Hooks After Simulation Step
        self._execute_callback(self.after_step())
        if time <= 0.0:
            self._execute_callback(self.before_end())
            raise StopIteration
        return self._model

    def __exit__(self, *a):
        """close"""
        if self._isStarted:
            self._model.swmm_end()
            self._isStarted = False
            # Execute Callback Hooks After Simulation End
            self._execute_callback(self.after_end())
        if self._isOpen:
            self._model.swmm_close()
            self._isOpen = False
            # Execute Callback Hooks After Simulation Closes
            self._execute_callback(self.after_close())

    @staticmethod
    def _is_callback(callable_object):
        """Checks if arugment is a function/method."""
        if not callable(callable_object):
            error_msg = 'Requires Callable Object, not {}'.format(
                type(callable_object))
            raise (PYSWMMException(error_msg))
        else:
            return True

    def _execute_callback(self, callback):
        """Runs the callback."""
        if callback:
            try:
                callback()
            except PYSWMMException:
                error_msg = "Callback Failed"
                raise PYSWMMException((error_msg))

    def initial_conditions(self, init_conditions):
        """
        Intial Conditions for Hydraulics and Hydrology can be set
        from within the api by setting a function to the
        initial_conditions property.

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
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
        if self._is_callback(init_conditions):
            self._initial_conditions = init_conditions

    def before_start(self):
        """Get Before Start Callback.

        :return: Callbacks
        """
        return self._callbacks["before_start"]

    def add_before_start(self, callback):
        """
        Add callback function/method/object to execute before
        the simlation starts. Needs to be callable.

        :param func callback: Callable Object

        >>> from pyswmm import Simulation
        >>>
        >>> def test_callback():
        ...     print("CALLBACK - Executed")
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...
        ...     sim.before_start(test_callback) #<- pass function handle.
        ...     print("Waiting to Start")
        ...     for ind, step in enumerate(sim):
        ...         print("Step {}".format(ind))
        ...     print("Complete!")
        ... print("Closed")
        "Waiting to Start"
        "CALLBACK - Executed"
        "Step 0"
        "Step 1"
        "Complete!"
        "Closed"
        """
        if self._is_callback(callback):
            self._callbacks["before_start"] = callback

    def before_step(self):
        """Get Before Step Callback.

        :return: Callbacks
        """
        return self._callbacks["before_step"]

    def add_before_step(self, callback):
        """
        Add callback function/method/object to execute before
        a simlation step. Needs to be callable.

        :param func callback: Callable Object

        (See self.add_before_start() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["before_step"] = callback

    def after_step(self):
        """Get After Step Callback.

        :return: Callbacks
        """
        return self._callbacks["after_step"]

    def add_after_step(self, callback):
        """
        Add callback function/method/object to execute after
        a simlation step. Needs to be callable.

        :param func callback: Callable Object

        (See self.add_before_start() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["after_step"] = callback

    def before_end(self):
        """Get Before End Callback.

        :return: Callbacks
        """
        return self._callbacks["before_end"]

    def add_before_end(self, callback):
        """
        Add callback function/method/object to execute after
        the simulation ends. Needs to be callable.

        :param func callback: Callable Object

        (See self.add_before_start() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["before_end"] = callback

    def after_end(self):
        """Get After End Callback.

        :return: Callbacks
        """
        return self._callbacks["after_end"]

    def add_after_end(self, callback):
        """
        Add callback function/method/object to execute after
        the simulation ends. Needs to be callable.

        :param func callback: Callable Object

        (See self.add_before_start() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["after_end"] = callback

    def after_close(self):
        """Get After Close Callback.

        :return: Callbacks
        """
        return self._callbacks["after_close"]

    def add_after_close(self, callback):
        """
        Add callback function/method/object to execute after
        the simulation is closed. Needs to be callable.

        :param func callback: Callable Object

        (See self.add_before_start() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["after_close"] = callback

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
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     sim.step_advance(30)
        ...     for step in sim:
        ...         print(sim.current_time)
        ...         # or here! sim.step_advance(newvalue)
        ...     sim.report()
        2015-11-01 14:00:30
        2015-11-01 14:01:00
        2015-11-01 14:01:30
        2015-11-01 14:02:00
        """
        self._advance_seconds = advance_seconds

    def terminate_simulation(self):
        """
        Inserts a request to stop a simulation and cleanly executing the callbacks.

        Examples:

        with Simulation("model") as sim:
            nodeXYZ = Nodes(sim)["nodeZYX"]

            def before_step_callback():
                if nodeXYZ.depth > 8:
                    sim.terminate_simulation()

            # Setting Callbacks
            sim.add_before_step(before_step_callback)

            for ind, step in enumerate(sim):
                # Now simulation will end early if the depth is > 8
                pass
        """
        self._terminate_request = True

    def report(self):
        """
        Writes to report file after simulation.

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
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
        >>> sim = Simulation('tests/data/model_weir_setting.inp')
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

        >>> sim = Simulation('tests/data/model_weir_setting.inp')
        >>> sim.execute()
        """
        self._model.swmmExec()

    @property
    def engine_version(self):
        """
        Retrieves the SWMM Engine Version.

        :return: Engine Version
        :rtype: LooseVersion

        Examples:

        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     print(sim.engine_version)
        5.1.14
        """
        return self._model.swmm_getVersion()

    @property
    def runoff_error(self):
        """
        Retrieves the Runoff Mass Balance Error.

        :return: Runoff Mass Balance Error
        :rtype: float

        Examples:

        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...    sim.execute()
        ...    print(sim.runoff_error)
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

        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...    sim.execute()
        ...    print(sim.flow_routing_error)
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

        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...    sim.execute()
        ...    print(sim.quality_error)
        0.01
        """
        return self._model.swmm_getMassBalErr()[2]

    @property
    def start_time(self):
        """Get/set Simulation start time.

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     print(sim.start_time)
        ...     sim.start_time = datetime(2015,5,10,15,15,1)
        datetime.datetime(2015,5,10,15,15,1)
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
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     print(sim.end_time)
        ...     sim.end_time = datetime(2016,5,10,15,15,1)
        datetime.datetime(2016,5,10,15,15,1)
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
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     print(sim.report_start)
        ...     sim.report_start = datetime(2015,5,10,15,15,1)
        datetime.datetime(2015,5,10,15,15,1)
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
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     print(sim.flow_units)
        CFS
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
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     print(sim.system_units)
        US
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
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     for step in sim:
        ...         print(sim.current_time)
        ...     sim.report()
        2015-11-01 14:00:30
        2015-11-01 14:01:00
        2015-11-01 14:01:30
        2015-11-01 14:02:00
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
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     for step in sim:
        ...         print(sim.percent_complete)
        ...     sim.report()
        0.01
        0.25
        0.50
        0.75
        """
        dt = self.current_time - self.start_time
        total_time = self.end_time - self.start_time
        return float(dt.total_seconds()) / total_time.total_seconds()
