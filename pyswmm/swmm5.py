# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""
Python extensions for the SWMM5 Programmers toolkit.

Open Water Analytics (http://wateranalytics.org/)
"""

# Standard library imports
import distutils.version
import sys
from datetime import datetime

# Third party imports
from swmm.toolkit import solver

# Local imports
import pyswmm.toolkitapi as tka


class SWMMException(Exception):
    """Custom exception class for SWMM errors."""

    def __init__(self, error_code, error_message):
        self.warning = False
        self.args = (error_code, )
        self.message = error_message

    def __str__(self):
        return self.message


class PYSWMMException(Exception):
    """Custom exception class for PySWMM errors."""

    def __init__(self, error_message):
        self.warning = False
        self.message = error_message

    def __str__(self):
        return self.message


class PySWMM(object):
    """
    Wrapper class to lead SWMM DLL object.

    This allow performing operations on the SWMM object that is created when
    the file is being loaded.

    PySWMM can be run in two different modes:

    Mode 1: Execute simulation without any intervention

    * Open the Input file using swmm_open()
    * Execute the simlation without intervening swmmExec()
    * then close calling swmm_close()

    Examples:

    >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
    >>> swmm_model.swmm_open()
    >>> swmm_model.swmmExec()
    >>> swmm_model.swmm_close()

    ---or---

    Mode 2: Step through the entire simulation manually by (This mode allows
    the user to invervene and stream simulation data as well as set parameters
    and use outside controls approaches)

    * swmm_open()
    * swmm_start()
    * swmm_step() or swmm_stride() until it returns 0
    * swmm_end()
    * swmm_report()
    * swmm_close()

    Examples:

    >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
    >>> swmm_model.swmm_open()
    >>> swmm_model.swmm_start()
    >>> while(True):
    ...     time = swmm_model.swmm_step() # or swmm_stride()
    ...     if (time <= 0.0): break
    >>>
    >>> swmm_model.swmm_end()
    >>> swmm_model.swmm_report()
    >>> swmm_model.swmm_close()
    """

    def __init__(self,
                 inpfile='',
                 rptfile=None,
                 binfile=None,
                 swmm_lib_path=None):
        """
        Initialize the PySWMM object class.

        User can specified SWMM library path. Uses default lib if
        not provided.

        :param str inpfile: Name of SWMM input file (default '')
        :param str rptfile: Report file to generate (default None)
        :param str binfile: Optional binary output file (default None)
        :param str swmm_lib_path: SWMM library path (default None).

        """
        self.fileLoaded = False
        self.inpfile = inpfile
        self.rptfile = rptfile
        self.binfile = binfile

        self.curSimTime = 0.0

    def swmmExec(self, inpfile=None, rptfile=None, binfile=None):
        """
        Open an input file, run SWMM, then close the file.

        :param str inpfile: Name of SWMM input file
        :param str rptfile: Report file to generate
        :param str binfile: Optional binary output file

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmmExec()
        >>> swmm_model.swmm_close()
        """
        if inpfile is None:
            inpfile = self.inpfile

        if rptfile is None:
            if self.rptfile != '' and self.rptfile is not None:
                rptfile = self.rptfile
            else:
                rptfile = self.inpfile.replace('.inp', '.rpt')

        if binfile is None:
            if self.binfile != '' and self.binfile is not None:
                binfile = self.binfile
            else:
                binfile = self.inpfile.replace('.inp', '.out')

        sys.stdout.write("\n... SWMM Version {}".format(self.swmm_getVersion(
        )))

        try:
            self.swmm_run()
            sys.stdout.write("\n... Run Complete")
        except PYSWMMException:
            sys.stdout.write("\n\n... SWMM completed. There are errors.\n")
            raise (PYSWMMException("SWMM Close Failed"))

    def swmm_run(self, inpfile=None, rptfile=None, binfile=None):
        """# TODO:."""
        if inpfile is None:
            inpfile = self.inpfile

        if rptfile is None:
            if self.rptfile != '' and self.rptfile is not None:
                rptfile = self.rptfile
            else:
                rptfile = self.inpfile.replace('.inp', '.rpt')

        if binfile is None:
            if self.binfile != '' and self.binfile is not None:
                binfile = self.binfile
            else:
                binfile = self.inpfile.replace('.inp', '.out')

        solver.swmm_run(inpfile, rptfile, binfile)

    def swmm_open(self, inpfile=None, rptfile=None, binfile=None):
        """
        Opens SWMM input file & reads in network data.

        :param str inpfile: Name of SWMM input file
        :param str rptfile: Report file to generate
        :param str binfile: Optional binary output file

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_close()
        """
        if self.fileLoaded:
            self.swmm_close()
            error_msg = 'Fatal error closing previously opened file'
            raise (PYSWMMException(error_msg))

        if inpfile is None:
            inpfile = self.inpfile

        if rptfile is None:
            if self.rptfile != '' and self.rptfile is not None:
                rptfile = self.rptfile
            else:
                rptfile = self.inpfile.replace('.inp', '.rpt')
                self.rptfile = rptfile

        if binfile is None:
            if self.binfile != '' and self.binfile is not None:
                binfile = self.binfile
            else:
                binfile = self.inpfile.replace('.inp', '.out')
                self.binfile = binfile

        solver.swmm_open(inpfile, rptfile, binfile)
        self.fileLoaded = True

    def swmm_start(self, SaveOut2rpt=False):
        """
        Prepares to Start SWMM Simulation.

        :param bool SaveOut2rpt: Save timeseries results to rpt file
                                 (default is False).

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     if (time <= 0.0): break
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        solver.swmm_start(SaveOut2rpt)

    def swmm_end(self):
        """
        Ends SWMM Simulation.

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     if (time <= 0.0): break
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        solver.swmm_end()

    def swmm_step(self):
        """
        Advances SWMM Simulation by a single routing step.

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     if (time <= 0.0): break
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        return solver.swmm_step()

    def swmm_stride(self, advanceSeconds):
        """
        This function allows for user defined stride length to advance
        the model simulation by a defined time.  This is useful when control
        rules are managed externally by PySWMM. Instead of evaluating rules
        every routing step, instead the simulation can be advanced further
        in time before the PySWMM can intervene. When a 0 is returned, the
        simulation period has reached the end.

        :param int advanceSeconds: Number seconds to advance the simulation
                                   forward.
        :return: Current simulation time after a stride in decimal days (float)
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_stride(600)
        ...     if (time <= 0.0): break
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        ctime = self.curSimTime
        secPday = 3600.0 * 24.0
        advanceDays = advanceSeconds / secPday
        eps = advanceDays * 0.00001
        elapsed_time = 0

        while self.curSimTime <= ctime + advanceDays - eps:
            elapsed_time = solver.swmm_step()
            if elapsed_time == 0:
                return 0.0
            self.curSimTime = elapsed_time

        return elapsed_time

    def swmm_report(self):
        """
        Copies Time Series results from .out to .rpt file.

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     if (time <= 0.0): break
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        solver.swmm_report()

    def swmm_close(self):
        """
        Closes model and supporting files and cleans up memory.

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     if (time <= 0.0): break
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        solver.swmm_close()
        self.fileLoaded = False

    def swmm_getVersion(self):
        """
        Retrieves version number of current SWMM engine.

        The format used is xyzzz where x = major version number,
        y = minor version number, and zzz = build number.

        :return: version number of the DLL source code
        :rtype: int
        """
        major, minor, patch = solver.swmm_version_info().split('.')
        return distutils.version.LooseVersion('.'.join([major, minor, patch]))

        return
    def swmm_getMassBalErr(self):
        """
        Get Mass Balance Errors.

        :return: Runoff Error, Flow Routing Error, Quality Error
        :rtype: tuple
        """
        return solver.swmm_get_mass_balance()

    # --- NETWORK API FUNCTIONS
    # -------------------------------------------------------------------------
    def getSimulationDateTime(self, timeType):
        """
        Get Simulation Time Data (Based on SimulationTime options).

        :param int timeType: (toolkitapi.SimulationTime member variable)
        :return: datetime
        :rtype: datetime

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSimulationDateTime(SimulationTime.StartDateTime)
        2015-11-01 14:00:00
        >>> swmm_model.getSimulationDateTime(SimulationTime.EndDateTime)
        2015-11-04 00:00:00
        >>> swmm_model.getSimulationDateTime(SimulationTime.ReportStart)
        2015-11-01 14:00:00
        >>>
        >>> swmm_model.swmm_close()
        """
        return datetime(*solver.simulation_get_datetime(timeType))

    def setSimulationDateTime(self, timeType, newDateTime):
        """
        Set Simulation Time Data (Based on SimulationTime options).

        :param int timeType: (toolkitapi.SimulationTime member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setSimulationDateTime(SimulationTime.StartDateTime,
                                             datetime(2009, 10, 1, 12,30))
        >>>
        """
        solver.simulation_set_datetime(timeType, newDateTime.year, newDateTime.month, 
            newDateTime.day, newDateTime.hour, newDateTime.minute, newDateTime.second)

    def getSimUnit(self, unit_type):
        """
        Get Simulation Units.

        :param int unittype: Simulation Unit Type
        :return: Simulation Unit Type
        :rtype: str

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSimUnit(SimulationUnits.FlowUnits)
        CFS
        >>> swmm_model.swmm_close()
        """
        value = solver.simulation_get_unit(unit_type)

        if unit_type == tka.SimulationUnits.FlowUnits.value:
            # Temporary Solution (2017-1-2 BEM)
            _flowunitnames = ["CFS", "GPM", "MGD", "CMS", "LPS", "MLD"]
            return _flowunitnames[value]

        elif unit_type == tka.SimulationUnits.UnitSystem.value:
            # Temporary Solution (2017-1-2 BEM)
            _flowunitnames = ["US", "SI"]
            return _flowunitnames[value]

    def getSimOptionSetting(self, setting_type):
        """
        Get Simulation Option Settings.

        :param int settingtype: Analysis Option Setting
        :return: Simulation Analysis option setting
        :rtype: bool

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSimAnalysisSetting(SimAnalysisSettings.AllowPonding)
        False
        >>> swmm_model.swmm_close()
        """
        return bool(solver.simulation_get_setting(setting_type))

    def getSimAnalysisSetting(self, param_type):
        """
        Get Simulation Configuration Parameter.

        :param int paramtype: Simulation Parameter Type
        :return: Simulation Analysis Parameter Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSimAnalysisSetting(SimulationParameters.RouteStep)
        300
        >>> swmm_model.swmm_close()
        """
        return solver.simulation_get_parameter(param_type)

    def getProjectSize(self, object_type):
        """
        Get Project Size: Number of Objects.

        :param int objecttype: (member variable)
        :return: Object Count
        :rtype: int

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getProjectSize(ObjectType.NODE)
        10
        >>> swmm_model.swmm_close()
        """
        return solver.project_get_count(object_type)

    def getObjectId(self, objecttype, index):
        """
        Get Object ID name.

        :param int objecttype: (member variable)
        :param index: ID Index
        :return: Object ID
        :rtype: string

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getObjectId(ObjectType.NODE,35)
        "example_id_name"
        >>>
        >>> swmm_model.swmm_close()
        """
        return solver.project_get_id(objecttype, index)

    def getObjectIDList(self, objecttype):
        """
        Get Object ID list.

        :param int objecttype: (member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getObjectIDList(ObjectType.LINK)
        ['C1:C2', 'C2', 'C3']
        >>>
        >>> swmm_model.swmm_close()
        >>>
        """
        IDS = []
        for index in range(self.getProjectSize(objecttype)):
            IDS.append(self.getObjectId(objecttype, index))
        return IDS

    def getObjectIDIndex(self, objecttype, ID):
        """Get Object ID Index. Mostly used as an internal function."""
        return solver.project_get_index(objecttype, ID)

    def ObjectIDexist(self, objecttype, ID):
        """Check if Object ID Exists. Mostly used as an internal function."""
        index = solver.project_get_index(objecttype, ID)

        if index != -1:
            return True
        else:
            return False

    def getNodeType(self, ID):
        """
        Get Node Type (e.g. Junction, Outfall, Storage, Divider).

        :param str index: ID
        :return: Object ID
        :rtype: int

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getNodeType('J1')
        0
        >>>
        >>> swmm_model.getNodeType('J1') is NodeType.junction
        True
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        return solver.node_get_type(index)

    def getLinkType(self, ID):
        """
        Get Link Type (e.g. Conduit, Pump, Orifice, Weir, Outlet).

        :param str index: ID
        :return: Object ID
        :rtype: int

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLinkType('C1')
        3
        >>>
        >>> swmm_model.getLinkType('C1') is LinkType.weir
        True
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        return solver.link_get_type(index)

    def getLinkConnections(self, ID):
        """
        Get Link Connections (Upstream and Downstream Nodes).

        Interestingly, if the dynamic wave solver is used, when the input file
        is parsed and added to the SWMM5 data model, any negatively sloped
        conduits are reversed automatically. The swmm_getLinkConnections
        function always calls the _swmm_getLinkDirection function to ensure
        the user-assigned upstream ID and downstream IDs are in the correct
        order. This way, the function provides support for directed graphs
        automatically.

        :param str index: ID
        :return: (Upstream Node Index, Downstream Node Index)
        :rtype: tuple

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLinkConnections('C1')
        ('NodeUSID','NodeDSID')
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        us_node, ds_node = solver.link_get_connections(index)
        us_node_id = self.getObjectId(tka.ObjectType.NODE.value, us_node)
        ds_node_id = self.getObjectId(tka.ObjectType.NODE.value, ds_node)

        if self._getLinkDirection(ID) == 1:
            # Return Tuple of Upstream and Downstream Node IDS
            return us_node_id, ds_node_id
        # link validations reverse the conduit direction if the slope is < 0
        elif self._getLinkDirection(ID) == -1:
            # Return Tuple of Upstream and Downstream Node IDS
            return ds_node_id, us_node_id

    def _getLinkDirection(self, ID):
        """
        Internal Method: returns conduit flow direction.

        :param str index: link ID
        :return: 1 for conduit flow from upstream node to downstream node
        and -1 for conduit flow from downstream node to upstream node
        :rtype: int
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        return solver.link_get_direction(index)

    def getNodeParam(self, ID, parameter):
        """
        Get Node Parameter.

        :param str ID: Node ID
        :param int parameter: Parameter (toolkitapi.NodeParams member variable)
        :return: Parameter Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getNodeParam('J2',NodeParams.invertElev )
        13.392
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        return solver.node_get_parameter(index, parameter)

    def setNodeParam(self, ID, parameter, value):
        """
        Set Node Parameter.

        :param str ID: Node ID
        :param int Parameter: Parameter (toolkitapi.NodeParams member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getNodeParam('J2',NodeParams.invertElev, 19 )
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        solver.node_set_parameter(index, parameter, value)

    def getLinkParam(self, ID, parameter):
        """
        Get Link Parameter.

        :param str ID: Link ID
        :param int Parameter: Parameter (toolkitapi.NodeParams member variable)
        :return: Parameter Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLinkParam('C1:C2',LinkParams.offset1 )
        0.0
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        return solver.link_get_parameter(index, parameter)

    def setLinkParam(self, ID, parameter, value):
        """
        Set Link Parameter.

        :param str ID: Link ID
        :param int Parameter: Parameter (toolkitapi.NodeParams member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLinkParam('C1:C2',LinkParams.offset1, 2 )
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        solver.link_set_parameter(index, parameter, value)

    def getLidCOverflow(self, ID):
        """
        Get Lid Control Parameter.

        :param str ID: Lid Control ID
        :rtype: Bool

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLidCOverflow('J2')
        True
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LID.value, ID)
        return bool(solver.lid_control_get_overflow(index))

    def getLidCParam(self, ID, layer, parameter):
        """
        Get LidControl Parameter.

        :param str ID: Lid Control ID
        :param int layer: Layer (toolkitapi.LidLayers member variable)
        :param int parameter: Parameter (toolkitapi.LidLayersProperty member variable)
        :return: Parameter Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLidCParam('J2', LidLayer.surface, LidLayersProperty.thickness)
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LID.value, ID)
        return solver.lid_control_get_parameter(index, layer, parameter)

    def setLidCParam(self, ID, layer, parameter, value):
        """
        Set Lid Control Parameter Before/During Model Simulation.

        :param str ID: Lid Control ID
        :param int layer: Layer (toolkitapi.LidLayers member variable)
        :param int parameter: Parameter (toolkitapi.LidLayersProperty member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLidCParam('J2', LidLayer.surface, LidLayersProperty.thickness, 110)
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LID.value, ID)
        solver.lid_control_set_parameter(index, layer, parameter, value)

    def getLidUCount(self, ID):
        """
        Get Number of Lid Units Defined for Subcatchment.

        :param str ID: Subcatchment ID
        :rtype: int

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLidUCount('J2')
        2
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        return solver.lid_usage_get_count(index)

    def getLidUParam(self, subcatchID, lid_index, parameter):
        """
        Get LidUnit Parameter

        :param str subcatchID: Subcatchment ID
        :param int lid_index: Lid unit index
        :param int parameter: Paramter (toolkitapi.LidUParams member variable)
        :return: paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLidUParam('S2', 0, LidUParams.unitarea)
        1000
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        return solver.lid_usage_get_parameter(index, lid_index, parameter)

    def setLidUParam(self, subcatchID, lid_index, parameter, value):
        """
        Set LidUnit Parameter

        :param str subcatchID: Subcatchment ID
        :param int lid_index: Lid unit index
        :param int parameter: parameter (toolkitapi.LidUParams member variable)
        :param double value: value set to parameter
        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLidUParam('S2', 0, LidUParams.unitarea, 10)
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        solver.lid_usage_set_parameter(index, lid_index, parameter, value)

    def getLidUOption(self, subcatchID, lid_index, parameter):
        """
        Get LidUnit Option

        :param str subcatchID: Subcatchment ID
        :param int lid_index: Lid unit Index
        :param int parameter: paramter (toolkitapi.LidUParams member variable)
        :return: paramater Value
        :rtype: int

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLidUOption('S2', 0, LidUParams.index)
        1000
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        return solver.lid_usage_get_option(index, lid_index, parameter)

    def setLidUOption(self, subcatchID, lid_index, parameter, value):
        """
        Set LidUnit Option

        :param str subcatchID: Subcatchment ID
        :param int lid_index: Lid unit index
        :param int parameter: paramter (toolkitapi.LidUParams member variable)
        :param double value: value set to parameter
        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLidUOption('S2', 0, LidUParams.index, 0)
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        solver.lid_usage_set_option(index, lid_index, parameter, value)

    def getSubcatchParam(self, ID, parameter):
        """
        Get Subcatchment Parameter

        :param str ID: Subcatchment ID
        :param int Parameter: Parameter (toolkitapi.SubcParams member variable)
        :return: Parameter Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLinkParam('S2',SubcParams.area )
        43561.596096880996
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        return solver.subcatch_get_parameter(index, parameter)

    def setSubcatchParam(self, ID, parameter, value):
        """
        Set Subcatchment Parameter.

        :param str ID: Subcatchment ID
        :param int parameter: paramter (toolkitapi.SubcParams member variable)
        :param double value: value set to parameter

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLinkParam('S2',SubcParams.area, 100 )
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        solver.subcatch_set_parameter(index, parameter, value)

    def getSubcatchOutConnection(self, ID):
        """
        Get Subcatchment Outlet Connection.

        This function return the type of loading surface and the ID. The two
        load to objects are nodes and other subcatchments.

        Nodes are ObjectType.NODE
        Subcatchments are ObjectType.SUBCATCH

        :param str ID: Subcatchment ID
        :param int Parameter: Parameter (toolkitapi.SubcParams member variable)
        :return: (Loading Surface Type, ID)
        :rtype: tuple

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSubcatchOutConnection('S2',SubcParams.area )
        (2, 'J2')
        >>>
        >>> subout = swmm_model.getSubcatchOutConnection('S2',SubcParams.area )
        >>> subout[0]  == ObjectType.NODE
        True
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        outlet_type, outlet_index = solver.subcatch_get_connection(index)
        outlet_id = self.getObjectId(outlet_type, outlet_index)

        return outlet_id

    def getGagePrecip(self, ID, parameter):
        """
        Get precipitation from gage

        This function returns the rainfall, show and total precipitation
        associated with the gage

        :param str ID: Gage ID
        :param int parameter: paramter (toolkitapi.RainGageResults member variable)
        :return: value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getGagePrecip('Gage1', )
        0.0
        >>> swmm_model.swmm_close()

        """
        index = self.getObjectIDIndex(tka.ObjectType.GAGE.value, ID)
        return solver.raingage_get_precipitation(index, parameter)

    # --- Active Simulation Result "Getters"
    # -------------------------------------------------------------------------
    def getCurrentSimulationTime(self):
        """
        Get Current Simulation DateTime in Python Format.

        :return: Python Datetime
        :rtype: datetime

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print(swmm_model.getCurrentSimualationTime())
        ...     if (time <= 0.0): break
        2015-11-03 10:10:12
        2015-11-03 10:20:12
        2015-11-03 10:30:12
        2015-11-03 10:40:12
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        return datetime(*solver.simulation_get_current_datetime())

    def getLidUFluxRates(self, subcatchID, lidIndex, layerIndex):
        """
        Get Lid Unit Layer Flux Rates Result.

        :param str subcatchID: Subcatchment ID
        :param int lidIndex: Lid unit Index
        :param int layerIndex: Parameter (toolkitapi.LidLayers member variable)
        :return: Parameter Value
        :rtype: float
        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print(swmm_model.getLidUFluxRates('J1', 0, LidLayers.surface))
        ...     if (time <= 0.0): break
        1.2
        1.5
        1.9
        1.2
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(
            tka.ObjectType.SUBCATCH.value, subcatchID)
        return solver.lid_usage_get_flux_rate(index, lidIndex, layerIndex)

    def getLidUResult(self, subcatchID, lidIndex, resultType):
        """
        Get Lid Result.

        :param str subcatchID: Subcatchment ID
        :param int lidIndex: Lid unit Index
        :param int resultType: Parameter (toolkitapi.LidUResults member variable)
        :return: Parameter Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print(swmm_model.getLidUResult('J1', 0, LidUResults.inflow))
        ...     if (time <= 0.0): break
        1.2
        1.5
        1.9
        1.2
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(
            tka.ObjectType.SUBCATCH.value, subcatchID)
        return solver.lid_usage_get_result(index, lidIndex, resultType)

    def getLidGResult(self, subcatchID, resultType):
        """
        Get Lid Group Result.

        :param str subcatchID: Subcatchment ID
        :param int resultType: Parameter (toolkitapi.LidUResults member variable)
        :return: Parameter Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print(swmm_model.getLidGResult('J1', LidUResults.flowToPerv))
        ...     if (time <= 0.0): break
        1.2
        1.5
        1.9
        1.2
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        return solver.lid_group_get_result(index, resultType)

    def getNodeResult(self, ID, result_type):
        """
        Get Node Result.

        :param str ID: Node ID
        :param int result_type: parameter (toolkitapi.NodeResults member variable)
        :return: value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print(swmm_model.getNodeResult('J1', NodeResults.newDepth))
        ...     if (time <= 0.0): break
        1.2
        1.5
        1.9
        1.2
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        return solver.node_get_result(index, result_type)

    def getNodePollut(self, ID, result_type):
        """
        Get water quality results from a Node.

        :param str ID: Node ID
        :param int result_type: parameter (toolkitapi.NodePollut member value)
        :rtype: list
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        return solver.node_get_pollutant(index, result_type)

    def getLinkResult(self, ID, result_type):
        """
        Get Link Result.

        :param str ID: Link ID
        :param int result_type: parameter (toolkitapi.LinkResults member variable)
        :return: parameter value

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print(swmm_model.getLinkResult('J1', LinkResults.newFlow))
        ...     if (time <= 0.0): break
        1.2
        1.5
        1.9
        1.2
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        return solver.link_get_result(index, result_type)

    def getLinkPollut(self, ID, result_type):
        """
        Get water quality results from a Link.

        :param str ID: Link ID
        :param int result_type:  parameter (toolkitapi.LinkPollut member value)
        :return: Pollutant Value
        :rtype: list
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        return solver.link_get_pollutant(index, result_type)

    def getSubcatchResult(self, ID, result_type):
        """
        Get Subcatchment Result

        :param str ID: Subcatchment ID
        :param int result_type: paramter (toolkitapi.LinkResults member variable)
        :return: paramater Value

        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print(swmm_model.getSubcatchResult('S3', SubcResults.newRunoff))
        ...     if (time <= 0.0): break
        0.01
        0.05
        0.09
        0.08
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        return solver.subcatch_get_result(index, result_type)

    def getSubcatchPollut(self, ID, result_type):
        """
        Get pollutant results from a Subcatchment.

        :param str ID: Subcatchment ID
        :param int result_type: parameter (toolkitapi.SubcPollut member variable)
        :return: Pollutant Values
        :rtype: list
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        return solver.subcatch_get_pollutant(index, result_type)

    def node_statistics(self, ID):
        """
        Get stats for a Node.

        :param str ID: Node ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        stats = solver.node_get_stats(index)
        alias = tka.NodeStats._py_alias_ids
        # Copy Items to Dictionary using Alias Names.
        dict_stats = {}
        for attr in dir(stats):
            if "_" not in attr and attr in alias:
                dict_stats[alias[attr]] = getattr(stats, attr)
        return dict_stats

    def node_inflow(self, ID):
        """
        Get total inflow volume for a Node.

        :param str ID: Node ID
        :return: Total Volume
        :rtype: float
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        return solver.node_get_total_inflow(index)

    def storage_statistics(self, ID):
        """
        Get stats for a Storage Node.

        :param str ID: Node ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        stats = solver.storage_get_stats(index)
        alias = tka.StorageStats._py_alias_ids
        # Copy Items to Dictionary using Alias Names.
        dict_stats = {}
        for attr in dir(stats):
            if "_" not in attr and attr in alias:
                dict_stats[alias[attr]] = getattr(stats, attr)
        return dict_stats

    def outfall_statistics(self, ID):
        """
        Get stats for a Outfall Node.

        :param str ID: Node ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        stats = solver.outfall_get_stats(index)
        alias = tka.OutfallStats._py_alias_ids
        # Copy Items to Dictionary using Alias Names.
        dict_stats = {}
        for attr in dir(stats):
            if "_" not in attr and attr in alias:
                if attr == "totalLoad":
                    dict_stats[alias[attr]] = {}
                    pollutants = self.getObjectIDList(tka.ObjectType.POLLUT.value)
                    for index, pollutant in enumerate(pollutants):
                        dict_stats[alias[attr]][pollutant] = stats.get_totalLoad(index)
                else:
                    dict_stats[alias[attr]] = getattr(stats, attr)
        return dict_stats

    def conduit_statistics(self, ID):
        """
        Get stats for a Conduits.

        :param str ID: Conduit ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        stats = solver.link_get_stats(index)
        alias = tka.LinkStats._py_alias_ids
        # Copy Items to Dictionary using Alias Names.
        dict_stats = {}
        for attr in dir(stats):
            if "_" not in attr and attr in alias:
                dict_stats[alias[attr]] = getattr(stats, attr)
        return dict_stats

    def pump_statistics(self, ID):
        """
        Get stats for a Pump.

        :param str ID: Pump ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        stats = solver.pump_get_stats(index)
        alias = tka.PumpStats._py_alias_ids
        # Copy Items to Dictionary using Alias Names.
        dict_stats = {}
        for attr in dir(stats):
            if "_" not in attr and attr in alias:
                dict_stats[alias[attr]] = getattr(stats, attr)
        return dict_stats

    def subcatch_statistics(self, ID):
        """
        Get stats for a Subcatchment.

        :param str ID: Subcatchment ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        stats = solver.subcatch_get_stats(index)
        alias = tka.SubcStats._py_alias_ids
        # Copy Items to Dictionary using Alias Names.
        dict_stats = {}
        for attr in dir(stats):
            if "_" not in attr and attr in alias:
                dict_stats[alias[attr]] = getattr(stats, attr)
        return dict_stats

    def flow_routing_stats(self):
        """
        Get Flow Routing System stats.

        :return: Dictionary of Flow Routing Stats.
        :rtype: dict
        """
        stats = solver.system_get_routing_totals()
        alias = tka.RoutingTotals._py_alias_ids
        # Copy Items to Dictionary using Alias Names.
        dict_stats = {}
        for attr in dir(stats):
            if "_" not in attr and attr in alias:
                dict_stats[alias[attr]] = getattr(stats, attr)
        return dict_stats

    def runoff_routing_stats(self):
        """
        Get Runoff Routing System stats.

        :return: Dictionary of Runoff Routing Stats.
        :rtype: dict
        """
        stats = solver.system_get_runoff_totals()
        alias = tka.RunoffTotals._py_alias_ids
        # Copy Items to Dictionary using Alias Names.
        dict_stats = {}
        for attr in dir(stats):
            if "_" not in attr and attr in alias:
                dict_stats[alias[attr]] = getattr(stats, attr)
        return dict_stats

    # --- Active Simulation Parameter "Setters"
    # -------------------------------------------------------------------------
    def setLinkSetting(self, ID, target_setting):
        """
        Set Link Setting (Pumps, Orifices, Weirs).

        :param str ID: Link ID
        :param float target_setting: New target setting which will be applied
        at the start of the next routing step.

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> i = 0
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     i+=1
        ...     if i == 80:
        ...         swmm_model.setLinkSetting('C3',0.5)
        ...     if (time <= 0.0): break
        ...
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        solver.link_set_target_setting(index, target_setting)

    def setNodeInflow(self, ID, flow_rate):
        """
        Set Node Inflow rate.

        The flow rate should be in the user defined units. The value is held
        constant in the model until it is redefined by the toolkit API.

        :param str ID: Node ID
        :param float flow_rate: New flow rate in the user-defined flow units

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> i = 0
        >>> while(True):
        ...     if i == 80:
        ...         swmm_model.setNodeInflow('J1',4)
        ...     time = swmm_model.swmm_step()
        ...     i+=1
        ...     if (time <= 0.0): break
        ...
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        solver.node_set_total_inflow(index, flow_rate)

    def setOutfallStage(self, ID, stage):
        """
        Set Outfall Stage (head).

        The level should be in the user defined units. The value is held
        constant in the model until it is redefined by the toolkit API.

        :param str ID: Node ID
        :param float stage: New flow rate in the user-defined flow units

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> i = 0
        >>> while(True):
        ...     if i == 80:
        ...         swmm_model.setOutfallStage('J1',4)
        ...     time = swmm_model.swmm_step()
        ...     i+=1
        ...     if (time <= 0.0): break
        ...
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        solver.outfall_set_stage(index, stage)

    def setGagePrecip(self, ID, value):
        """
        Set precipitation to gage

        This function sets the rainfall intensity to the gage

        :param str ID: Gage ID
        :param float valve: rainfall intensity
        :return: errcode

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setGagePrecip('Gage1', 10.0)
        >>> swmm_model.swmm_close()

        """
        index = self.getObjectIDIndex(tka.ObjectType.GAGE.value, ID)
        solver.raingage_set_precipitation(index, value)

    def setNodePollut(self, ID, pollutant_ID, pollutant_value):
        """
        Set water quality results in a Node.

        :param str ID: Node ID
        :param str pollutant_ID
        :param float pollutant_value: pollutant value to set
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        pollutant_index = self.getObjectIDIndex(tka.ObjectType.POLLUT.value, pollutant_ID)
        solver.node_set_pollutant(index, tka.NodePollut.nodeQual.value, pollutant_index, pollutant_value)

    def setLinkPollut(self, ID, pollutant_ID, pollutant_value):
        """
        Set water quality results in a Link.

        :param str ID: Link ID
        :param str ID: Pollutant ID
        :param float pollutant_value: pollutant value to set
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        pollutant_index = self.getObjectIDIndex(tka.ObjectType.POLLUT.value, pollutant_ID)
        solver.link_set_pollutant(index, tka.LinkPollut.linkQual.value, pollutant_index, pollutant_value)

if __name__ == '__main__':
    test = PySWMM(
        inpfile=r"./tests/data/model_weir_setting.inp",
        rptfile=r"./tests/data/model_weir_setting.rpt",
        binfile=r"./tests/data/model_weir_setting.out")
    test.swmm_open()

    print("Simulation Time Info")
    print("Start Time")
    print(test.getSimulationDateTime(tka.SimulationTime.StartDateTime.value))
    print("End Time")
    print(test.getSimulationDateTime(tka.SimulationTime.EndDateTime.value))
    print("Report Time")
    print(test.getSimulationDateTime(tka.SimulationTime.ReportStart.value))

    print("Simulation Units")
    print(test.getSimUnit(tka.SimulationUnits.FlowUnits.value))

    print("Simulation Engine Version")
    print(test.swmm_getVersion())

    print("Simulation Allow Ponding Option Selection")
    print(
        test.getSimAnalysisSetting(tka.SimAnalysisSettings.AllowPonding.value),
    )

    print("Simulation Routing Step")
    print(test.getSimAnalysisSetting(tka.SimulationParameters.RouteStep.value))

    print("Number of Nodes")
    print(test.getProjectSize(tka.ObjectType.NODE.value))

    print("Node ID")
    IDS = test.getObjectIDList(tka.ObjectType.NODE.value)
    print(IDS)
    print('ID,Invert,Type')
    for ind, idd in enumerate(IDS):
        print(
            ind,
            idd,
            test.getNodeParam(idd, tka.NodeParams.invertElev.value),
            test.getNodeParam(idd, tka.NodeParams.fullDepth.value),
            test.getNodeType(idd), )

    print("Link ID")
    print('ID,offset1,LinkConnections')
    IDS = test.getObjectIDList(tka.ObjectType.LINK.value)
    print(IDS)
    for ind, idd in enumerate(IDS):
        print(
            ind,
            idd,
            test.getLinkParam(idd, tka.LinkParams.offset1.value),
            test.getLinkConnections(idd), )

    print("SUBCATCH ID")
    IDS = test.getObjectIDList(tka.ObjectType.SUBCATCH.value)
    print(IDS)
    for ind, idd in enumerate(IDS):
        print(
            ind,
            idd,
            test.getSubcatchParam(idd, tka.SubcParams.area.value),
            test.getSubcatchOutConnection(idd), )

    test.swmm_start(False)
    i = 0
    while True:
        if i % 1000 == 0:
            print("test {}".format(test.flow_routing_stats()))
        eltime = test.swmm_step()
        i += 1
        if eltime == 0:
            break

    test.swmm_end()
    test.swmm_close()
