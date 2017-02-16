# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Base class for a SWMM Simulation."""

from swmm5 import PySWMM

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
    >>> for ind, step in enumerate(sim):
    ...     pass
    >>>     
    >>> sim.report()
    >>> sim.close()

    Intialize using with statement.  This automatically cleans up
    after a simulation

    >>> from pyswmm import Simulation
    >>>       
    >>> with Simulation('./TestModel1_weirSetting.inp') as sim:
    ...     for ind, step in enumerate(sim):
    ...         pass
    ...     sim.report()

    Initialize the simulation and execute.  This style does not allow
    the user to interact with the simulation.  However, this approach
    tends to be the fastes. 

    >>> from pyswmm import Simulation
    >>>   
    >>> sim = Simulation('./TestModel1_weirSetting.inp')        
    >>> sim.execute()
    
    """

    def __init__(self, inputfile, reportfile = None, outputfile = None):
        self._model = PySWMM(inputfile, reportfile, outputfile)
        self._model.swmm_open()
        self._advance_seconds = None
        self._isStarted = False
        
    def __enter__(self):
        """
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     for ind, step in enumerate(sim):
        ...         print(step.getCurrentSimualationTime())
        ...     sim.report()
        >>>
        >>> 2015-11-01 14:00:01
        >>> 2015-11-01 14:00:02
        >>> 2015-11-01 14:00:03
        >>> 2015-11-01 14:00:04        
        """
        return self

    def __iter__(self):
        return self
    
    def next(self):
        # Start Simulation
        if not self._isStarted:
            self._model.swmm_start()
            self._isStarted = True
        # Simulation Step Amount
        if self._advance_seconds == None:
            time = self._model.swmm_step()
        else:
            time = self._model.swmm_stride(self._advance_seconds)
            
        if time <= 0.0:
            self._model.swmm_end()
            raise StopIteration
        return self._model

    def __exit__(self, *a):
        self._model.swmm_end()
        self._model.swmm_close()

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
        ...     for ind, step in enumerate(sim):
        ...         print(step.getCurrentSimualationTime())
        ...         # or here! sim.step_advance(newvalue)
        ...     sim.report()
        >>>
        >>> 2015-11-01 14:00:01
        >>> 2015-11-01 14:00:02
        >>> 2015-11-01 14:00:03
        >>> 2015-11-01 14:00:04
        """
        self._advance_seconds = advance_seconds

    def report(self):
        """
        Writes to report file after simulation
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     for ind, step in enumerate(sim):
        ...         pass
        ...     sim.report()        
        self._model.swmm_report()
        """

    def close(self):
        """
        Intialize a simulation and iterate through a simulation. This
        approach requires some clean up.
        
        Examples:

        >>> from pyswmm import Simulation
        >>>    
        >>> sim = Simulation('./TestModel1_weirSetting.inp')
        >>> for ind, step in enumerate(sim):
        ...     pass
        >>>     
        >>> sim.report()
        >>> sim.close()        
        """
        self.__exit__()
        
    def execute(self):
        """
        Open an input file, run SWMM, then close the file.

        >>> swmm_model = PYSWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmmExec()     
        """
        self._model.swmmExec()
        
    @property
    def starttime(self):
        """Get/set Simulation start time

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     print sim.sim_starttime
        ...     sim.sim_starttime = datetime(2015,5,10,15,15,1)
        >>>
        >>> datetime.datetime(2015,5,10,15,15,1)
        """
        return self._model.getSimulationDateTime(SimulationTime.StartDateTime)
    
    @starttime.setter
    def starttime(self):
        """Set simulation Start time"""
        self._model.setSimulationDateTime(SimulationTime.StartDateTime, dtimeval)

    @property
    def endtime(self):
        """Get/set Simulation end time

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     print sim.sim_endtime
        ...     sim.sim_endtime = datetime(2016,5,10,15,15,1)
        >>>
        >>> datetime.datetime(2016,5,10,15,15,1)
        """
        return self._model.getSimulationDateTime(SimulationTime.EndDateTime)
    
    @endtime.setter
    def endtime(self):
        """Set simulation End time"""
        self._model.setSimulationDateTime(SimulationTime.EndDateTime, dtimeval)

    @property
    def reportstart(self):
        """Get/set Simulation report start time

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     print sim.sim_reportstart
        ...     sim.sim_reportstart = datetime(2015,5,10,15,15,1)
        >>>
        >>> datetime.datetime(2015,5,10,15,15,1)
        """
        return self._model.getSimulationDateTime(SimulationTime.ReportStart)
    
    @reportstart.setter
    def reportstart(self):
        """Set simulation report start time"""
        self._model.setSimulationDateTime(SimulationTime.ReportStart, dtimeval)

    @property
    def flowunits(self):
        """Get Simulation Units (CFS, GPM, MGD, CMS, LPS, MLD)

        :return: Flow Unit 
        :rtype: str
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     print sim.flowunits
        >>>
        >>> CFS
        """
        return self._model.getSimUnit(SimulationUnits.FlowUnits)

    @property
    def systemunits(self):
        """Get system units (US, SI)

        :return: System Unit 
        :rtype: str
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     print sim.systemunits
        >>>
        >>> US
        """
        return self._model.getSimUnit(SimulationUnits.UnitSystem)
