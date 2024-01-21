# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2023 Bryant E. McDonnell (See AUTHORS)
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Base class for a SWMM Simulation."""

# Standard import
from warnings import warn

# Local imports
from pyswmm.swmm5 import PySWMM, PYSWMMException
from pyswmm.toolkitapi import SimulationTime, SimulationUnits


class Simulation(object):
    """
    Base class for a SWMM Simulation.

    The model object provides several options to run a simulation.

    Initialize the Simulation class.

    :param str inpfile: Name of SWMM input file (default '')
    :param str rptfile: Report file to generate (default None)
    :param str binfile: Optional binary output file (default None)
    :param SimulationPreConfig sim_preconfig: Optional Pre Config (default None)

    Examples:

    Intialize using with statement.  This automatically cleans up
    after a simulation

    .. code-block:: python

        from pyswmm import Simulation

        with Simulation('tests/data/model_weir_setting.inp') as sim:
            for step in sim:
                pass

    Initialize the simulation and execute. This style does not allow
    the user to interact with the simulation. However, this approach
    tends to be the fastest.

    .. code-block:: python

        from pyswmm import Simulation

        sim = Simulation('tests/data/model_weir_setting.inp')
        sim.execute()
    """

    def __init__(self,
                 inputfile,
                 reportfile=None,
                 outputfile=None,
                 sim_preconfig=None):
        # sim_config enables a find/replace to be fun on the source input file
        # to create the new INP file.
        if sim_preconfig:
            if not isinstance(sim_preconfig, SimulationPreConfig):
                raise (Exception("Invalid Simulation Preconfig Instance."))
            else:
                if not sim_preconfig.input_file:
                    sim_preconfig.input_file = inputfile
                inputfile = sim_preconfig.apply_changes()

        self._model = PySWMM(inputfile, reportfile, outputfile)
        self._model.swmm_open()
        self._isOpen = True
        self._advance_seconds = None
        self._isStarted = False
        self._terminate_request = False
        self._callbacks = {
            "before_start": None,
            "after_start": None,
            "before_step": None,
            "after_step": None,
            "before_end": None,
            "after_end": None,
            "after_close": None
        }

    def __enter__(self):
        """
        Examples:

        .. code-block:: python

            from pyswmm import Simulation

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                for step in sim:
                    print(sim.current_time)

        .. code-block::

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
        """Start Simulation (no longer suggested to user)."""
        if not self._isStarted:
            # Execute Callback Hooks Before Start
            self._execute_callback(self._before_start())
            self._model.swmm_start(True)
            # Execute Callback Hooks After Start
            self._execute_callback(self._after_start())
            self._isStarted = True

    def __next__(self):
        """Next"""
        # Start Simulation
        self.start()
        # Check if simulation termination request was made
        if self._terminate_request:
            self._execute_callback(self._before_end())
            raise StopIteration
        # Execute Callback Hooks Before Simulation Step
        self._execute_callback(self._before_step())
        # Simulation Step Amount
        if self._advance_seconds is None:
            time = self._model.swmm_step()
        else:
            time = self._model.swmm_stride(self._advance_seconds)
        # Execute Callback Hooks After Simulation Step
        self._execute_callback(self._after_step())
        if time <= 0.0:
            self._execute_callback(self._before_end())
            raise StopIteration
        return self._model

    def __exit__(self, *a):
        """close"""
        if self._isStarted:
            self._model.swmm_end()
            self._isStarted = False
            # Execute Callback Hooks After Simulation End
            self._execute_callback(self._after_end())
        if self._isOpen:
            self._model.swmm_close()
            self._isOpen = False
            # Execute Callback Hooks After Simulation Closes
            self._execute_callback(self._after_close())

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
        Starting in PySWMM-v2 this method/function is set to be
        deprecated.  For setting initial depths refer to the
        Simulation.add_before_start() callback. If the user's goal is to
        set the initial link settings, instead use Simulation.add_after_start().
        """
        warn('This method was deprecated in PySWMM-v2',
             DeprecationWarning, stacklevel=2)

    def step_advance(self, advance_seconds):
        """
        Advances the model by X number of seconds instead of
        intervening at every routing step.  This does not change
        the routing step for the simulation; only lets python take
        back control after each advance period.

        :param int advance_seconds: Seconds to Advance simulation

        Examples:

        .. code-block:: python

            from pyswmm import Simulation

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                sim.step_advance(30)
                for step in sim:
                    print(sim.current_time)

        .. code-block::

            >>> 2015-11-01 14:00:30
            >>> 2015-11-01 14:01:00
            >>> 2015-11-01 14:01:30
            >>> 2015-11-01 14:02:00
        """
        self._advance_seconds = advance_seconds

    def terminate_simulation(self):
        """
        Inserts a request to stop a simulation and cleanly executing the callbacks.

        Examples:

        .. code-block:: python

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
        Writes to report file after simulation (no longer suggested for user).

        Examples:

        .. code-block:: python

            from pyswmm import Simulation

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                for step in sim:
                    pass
                sim.report()
        """
        self._model.swmm_report()

    def close(self):
        """
        Intialize a simulation and iterate through a simulation. This
        approach requires some clean up. No longer recommended that the user
        call this function directly.
        """
        self.__exit__()

    def execute(self):
        """
        Open an input file, run SWMM, then close the file.

        Examples:

        .. code-block:: python

            sim = Simulation('tests/data/model_weir_setting.inp')
            sim.execute()
        """
        self._model.swmmExec()

    @property
    def engine_version(self):
        """
        Retrieves the SWMM Engine Version.

        :return: Engine Version
        :rtype: LooseVersion

        Examples:

        .. code-block:: python

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                print(sim.engine_version)

        .. code-block::

            >>> 5.1.14
        """
        return self._model.swmm_getVersion()

    @property
    def runoff_error(self):
        """
        Retrieves the Runoff Mass Balance Error.

        :return: Runoff Mass Balance Error
        :rtype: float

        Examples:

        .. code-block:: python

            with Simulation('tests/data/model_weir_setting.inp') as sim:
               sim.execute()
               print(sim.runoff_error)

        .. code-block::

            >>> 0.01
        """
        return self._model.swmm_getMassBalErr()[0]

    @property
    def flow_routing_error(self):
        """
        Retrieves the Flow Routing Mass Balance Error.

        :return: Flow Routing Mass Balance Error
        :rtype: float

        Examples:

        .. code-block:: python

            with Simulation('tests/data/model_weir_setting.inp') as sim:
               sim.execute()
               print(sim.flow_routing_error)

        .. code-block::

            >>> 0.01
        """
        return self._model.swmm_getMassBalErr()[1]

    @property
    def quality_error(self):
        """
        Retrieves the Quality Routing Mass Balance Error.

        :return: Quality Routing Mass Balance Error
        :rtype: float

        Examples:

        .. code-block:: python

            with Simulation('tests/data/model_weir_setting.inp') as sim:
               sim.execute()
               print(sim.quality_error)

        .. code-block::

            >>> 0.01
        """
        return self._model.swmm_getMassBalErr()[2]

    @property
    def start_time(self):
        """Get/set Simulation start time.

        Examples:

        .. code-block:: python

            from pyswmm import Simulation

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                print(sim.start_time)
                sim.start_time = datetime(2015,5,10,15,15,1)

        .. code-block::

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

        .. code-block:: python

            from pyswmm import Simulation

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                print(sim.end_time)
                sim.end_time = datetime(2016,5,10,15,15,1)

        .. code-block::

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

        .. code-block:: python

            from pyswmm import Simulation

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                print(sim.report_start)
                sim.report_start = datetime(2015,5,10,15,15,1)

        .. code-block::

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

        .. code-block:: python

            from pyswmm import Simulation

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                print(sim.flow_units)

        .. code-block::

            >>> CFS
        """
        return self._model.getSimUnit(SimulationUnits.FlowUnits.value)

    @property
    def system_units(self):
        """Get system units (US, SI).

        :return: System Unit
        :rtype: str

        Examples:

        .. code-block:: python

            from pyswmm import Simulation

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                print(sim.system_units)

        .. code-block::

            >>> US
        """
        return self._model.getSimUnit(SimulationUnits.UnitSystem.value)

    @property
    def current_time(self):
        """Get Simulation Current Time.

        :return: Current Simulation Time
        :rtype: Datetime

        Examples:

        .. code-block:: python

            from pyswmm import Simulation

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                for step in sim:
                    print(sim.current_time)

        .. code-block::

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

        .. code-block:: python

            from pyswmm import Simulation

            with Simulation('tests/data/model_weir_setting.inp') as sim:
                for step in sim:

        .. code-block::

            >>> 0.01
            >>> 0.25
            >>> 0.50
            >>> 0.75
        """
        dt = self.current_time - self.start_time
        total_time = self.end_time - self.start_time
        return float(dt.total_seconds()) / total_time.total_seconds()

    def use_hotstart(self, hotstart_file):
        """
        Use a hotstart file to initialize the simulation.

        This must be run before the simualation loop but within
        the simulation context manager.

        :param str hotstart_file: Path to hotstart file.

        .. code-block:: python

            with Simulation('model_weir_setting.inp') as sim:
                sim.use_hotstart("path_to_hotstart.hsf")

                for ind, step in enumerate(sim):
                    break

        """
        self._model.swmm_use_hotstart(hotstart_file)

    def save_hotstart(self, hotstart_file):
        """
        Save the current state of the model to a hotstart file.

        This can be run at any point during the simultion.

        :param str hotstart_file: Path to hotstart file.

        .. code-block:: python

            with Simulation('model_weir_setting.inp') as sim:
                for ind, step in enumerate(sim):
                    if ind == 10:
                        sim.save_hotstart('new_hsf.HSF')

        """
        self._model.swmm_save_hotstart(hotstart_file)

    def _before_start(self):
        """Get Before Start Callback.

        :return: Callbacks
        """
        return self._callbacks["before_start"]

    def add_before_start(self, callback):
        """
        Add callback function/method/object to execute before
        the simlation starts. Needs to be callable.

        :param func callback: Callable Object

        (See self.add_after_close() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["before_start"] = callback

    def _after_start(self):
        """Get After Start Callback.

        :return: Callbacks
        """
        return self._callbacks["after_start"]

    def add_after_start(self, callback):
        """
        Add callback function/method/object to execute after
        a simlation start. Needs to be callable.  This callback allows
        setting initial link target_settings (such as an orifice).

        :param func callback: Callable Object

        (See self.add_after_close() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["after_start"] = callback

    def _before_step(self):
        """Get Before Step Callback.

        :return: Callbacks
        """
        return self._callbacks["before_step"]

    def add_before_step(self, callback):
        """
        Add callback function/method/object to execute before
        a simlation step. Needs to be callable.

        :param func callback: Callable Object

        (See self.add_after_close() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["before_step"] = callback

    def _after_step(self):
        """Get After Step Callback.

        :return: Callbacks
        """
        return self._callbacks["after_step"]

    def add_after_step(self, callback):
        """
        Add callback function/method/object to execute after
        a simlation step. Needs to be callable.

        :param func callback: Callable Object

        (See self.add_after_close() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["after_step"] = callback

    def _before_end(self):
        """Get Before End Callback.

        :return: Callbacks
        """
        return self._callbacks["before_end"]

    def add_before_end(self, callback):
        """
        Add callback function/method/object to execute after
        the simulation ends. Needs to be callable.

        :param func callback: Callable Object

        (See self.add_after_close() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["before_end"] = callback

    def _after_end(self):
        """Get After End Callback.

        :return: Callbacks
        """
        return self._callbacks["after_end"]

    def add_after_end(self, callback):
        """
        Add callback function/method/object to execute after
        the simulation ends. Needs to be callable.

        :param func callback: Callable Object

        (See self.add_after_close() for more details)
        """
        if self._is_callback(callback):
            self._callbacks["after_end"] = callback

    def _after_close(self):
        """Get After Close Callback.

        :return: Callbacks
        """
        return self._callbacks["after_close"]

    def add_after_close(self, callback):
        """
        Add callback function/method/object to execute after
        the simulation is closed. Needs to be callable.

        :param func callback: Callable Object

        .. code-block:: python

            from pyswmm import Simulation

            def test_callback():
                print("CALLBACK - Executed")

            with Simulation('tests/data/model_weir_setting.inp') as sim:

                sim.before_start(test_callback) #<- pass function handle.
                print("Waiting to Start")
                for ind, step in enumerate(sim):
                    print("Step {}".format(ind))
                print("Complete!")
            print("Closed")

        .. code-block::

            >>> "Waiting to Start"
            >>> "CALLBACK - Executed"
            >>> "Step 0"
            >>> "Step 1"
            >>> "Complete!"
            >>> "Closed"
        """
        if self._is_callback(callback):
            self._callbacks["after_close"] = callback


class SimulationPreConfig():
    """
    This class was developed to introduce a simple way to programmatically
    adjust nearly all model parameters. Once the user instantiates the
    `SimulationPreConfig` object the method `add_update_by_token` can be called
    for each parameter (by index) that they would like to update. The parameter
    limits are still up to the user to get right as per the SWMM user's guide.

    The arguments are as follows.  In the Base INP file:

    .. code-block:: python

        [SUBCATCHMENTS]
        ;;                                         Total   Pcnt. Pcnt.  Curb
        ;;Name   Raingage         Outlet   Area    Imperv  Width Slope  Length
        ;;------ ---------------- -------- ------- ------- ----- ------ --------
        S1       SCS_24h_Type_I_1in J1     1       100     500   0.5    0


    .. code-block:: python

        from pyswmm import Simulation, SimulationPreConfig, Subcatchments

        # Create Config Handle
        sim_conf = SimulationPreConfig()

        # Specifying the update parameters
        # Parameter Order:
        # New Value, Section, Object ID, Parameter Index, Obj Row Num (optional)
        sim_conf.add_update_by_token("J2", "SUBCATCHMENTS", "S1", 2)
        sim_conf.add_update_by_token(2, "TIMESERIES", "SCS_24h_Type_I_1in", 2, 5)

        with Simulation(<path-to-inp>, sim_preconfig = sim_conf) as sim:
            S1 = Subcatchments(sim)["S1"]
            print(S1.connection)

            for step in sim:
                pass

    .. code-block:: python

        >>> (2, 'J2')

    In the New INP file:

    .. code-block:: python

        [SUBCATCHMENTS]
        ;;                                         Total   Pcnt. Pcnt.  Curb
        ;;Name   Raingage         Outlet   Area    Imperv  Width Slope  Length
        ;;------ ---------------- -------- ------- ------- ----- ------ --------
        S1       SCS_24h_Type_I_1in J3     1       100     500   0.5    0

    """

    def __init__(self):
        self._filename_suffix = "_mod"
        self._modifications = {}
        self._source_input_name = None

    @property
    def input_file(self):
        """
        This is set by the `Simulation` class but can also be set directly
        if the user wants to simply use this class for find replace.

        Examples:

        .. code-block:: python

            sim_conf = SimulationPreConfig()
            sim_conf.input_file = "./model_weir_setting.inp"

        .. code-block::

            >>> datetime.datetime(2016,5,10,15,15,1)
        """
        self._source_input_name

    @input_file.setter
    def input_file(self, inp_path):
        """"""
        self._source_input_name = inp_path

    @property
    def filename_suffix(self):
        """
        If the user wants to modify the new file name simply use this class
        for find replace.

        Examples:

        .. code-block:: python

            sim_conf = SimulationPreConfig()
            sim_conf.filename_suffix = "_a"

        .. code-block::

            >>> datetime.datetime(2016,5,10,15,15,1)
        """
        return self._filename_suffix

    @filename_suffix.setter
    def filename_suffix(self, suffix: str):
        """"""
        self._filename_suffix = suffix

    def add_update_by_token(self, new_val, section: str, id: str,
                            index: int, row_num=0):
        """
        This method allows the user to give the parmeter to be updated and
        where this value should be set in the input file.

        :param new_val: The new value (can be any normal data type)
        :param str section: Section name (such as "JUNCTIONS")
        :param str id: the SWMM object ID name (such as "J1")
        :param int index: The index of the parameter in the row to update (0 is first index)
        :param ind row_num: If multiple rows exist for an object like "HYDROGRAPHS" (0 is first index)

        .. code-block:: python

            from pyswmm import SimulationPreConfig

            # Create Config Handle
            sim_conf = SimulationPreConfig()

            # Specifying the update parameters
            # Parameter Order:
            # New Value, Section, Object ID, Parameter Index, Obj Row Num (optional)
            sim_conf.add_update_by_token("J2", "SUBCATCHMENTS", "S1", 2)
            sim_conf.add_update_by_token(2, "TIMESERIES", "SCS_24h_Type_I_1in", 2, 5)

        """
        section = section.lower()
        id = id.lower()

        if section not in self._modifications.keys():
            self._modifications[section] = {}
        if id not in self._modifications[section].keys():
            self._modifications[section][id] = {}
        if row_num not in self._modifications[section][id.lower()].keys():
            self._modifications[section][id][row_num] = {}

        self._modifications[section][id][row_num][index] = new_val

    def apply_changes(self):
        """
        If the user wants to modify the new file name simply use this class
        for find replace then Apply those changes.

        Examples:

        .. code-block:: python

            sim_conf = SimulationPreConfig()
            sim_conf.input_file = "./model_weir_setting.inp"
            sim_conf.filename_suffix = "_a"

            sim_conf.apply_changes()

        .. code-block::

            >>> datetime.datetime(2016,5,10,15,15,1)

        """
        mods = self._modifications
        if not self._source_input_name:
            raise (Exception("No Source INP set"))

        def write_line(fl_handle, ln):
            end = ''
            if not ln.endswith("\n"):
                end = '\n'
            fl_handle.write(ln+end)

        dest_file = self._source_input_name[:-4] \
            + self._filename_suffix + '.inp'

        fl_source = open(self._source_input_name, 'r')
        fl_destin = open(dest_file, 'w')

        section_replacements = False
        section = None
        id_ref = None
        row_count = 0

        for ln in fl_source:
            if '[' in ln and ']' in ln:
                ln_orig = ln
                ln = ln.strip()
                ln = ln.replace("[", '')
                ln = ln.replace("]", '')
                section = ln.lower()
                section_replacements = False
                # Only modify sections if there are edits.
                if section in mods.keys():
                    section_replacements = True
                id_ref = None
                row_count = 0
                write_line(fl_destin, ln_orig)
            elif ln.startswith(';') or len(ln.split()) == 0:
                write_line(fl_destin, ln)
            elif not section_replacements:
                write_line(fl_destin, ln)
            else:
                ln = ln.strip()
                ln_split = ln.split()
                if id_ref == ln_split[0].lower():
                    row_count += 1
                else:
                    id_ref = ln_split[0].lower()
                    row_count = 0

                ln_mod = ln_split
                if id_ref in mods[section].keys():
                    if row_count in mods[section][id_ref].keys():
                        for index in mods[section][id_ref][row_count].keys():
                            if index >= 0 and index < len(ln_split):
                                ln_mod[index] = mods[section][id_ref][row_count][index]
                                ln_out = "     ".join([str(v) for v in ln_mod])
                            else:
                                raise (Exception("{0} {1} {2} index {3} out of bounds".format(
                                    section, id_ref,
                                    row_count, index)))
                    else:
                        ln_out = ln
                else:
                    ln_out = ln
                write_line(fl_destin, ln_out)
        fl_source.close()
        fl_destin.close()

        return dest_file
