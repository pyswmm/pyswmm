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
from datetime import datetime
import ctypes
import distutils.version
import os
import sys
import warnings
import struct

# Third party imports
import six

# Local imports
from pyswmm.lib import DLL_SELECTION
import pyswmm.toolkitapi as tka

# Local variables
SWMM_VER_51011 = '5.1.13'


class SWMMException(Exception):
    """Custom exception class for SWMM errors."""

    def __init__(self, error_code, error_message):
        self.warning = False
        self.args = (error_code, )
        self.message = error_message

    def __str__(self):
        return self.message


class PYSWMMException(Exception):
    """Custom exception class for PySWMM errors. """

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

        if not swmm_lib_path:
            swmm_lib_path = DLL_SELECTION()
        
        if os.name == 'nt':
            # Windows Support
            self.SWMMlibobj = ctypes.WinDLL(swmm_lib_path)

        if sys.platform == 'darwin':
            # Mac Osx Support
            self.SWMMlibobj = ctypes.cdll.LoadLibrary(swmm_lib_path)

        if sys.platform.startswith('linux'):
            # Linux Support
            self.SWMMlibobj = ctypes.CDLL(swmm_lib_path)

    def _error_message(self, errcode):
        """
        Returns SWMM Error Message.

        :param int errcode: SWMM error code index
        :return: Error Message from SWMM
        :rtype: str
        """
        errcode = ctypes.c_int(errcode)
        _errmsg = ctypes.create_string_buffer(257)
        self.SWMMlibobj.swmm_getAPIError(errcode, _errmsg)
        print(_errmsg.value.decode("utf-8"))
        return _errmsg.value.decode("utf-8")

    def _error_check(self, errcode):
        """
        Checks SWMM Error Message and raises Exception.

        :param int errcode: SWMM error code index
        """

        if errcode != 0:
            raise SWMMException(errcode, self._error_message(errcode))

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

        self.SWMMlibobj.swmm_run(
            ctypes.c_char_p(six.b(inpfile)),
            ctypes.c_char_p(six.b(rptfile)), ctypes.c_char_p(six.b(binfile)))

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

        errcode = self.SWMMlibobj.swmm_open(
            ctypes.c_char_p(six.b(inpfile)),
            ctypes.c_char_p(six.b(rptfile)), ctypes.c_char_p(six.b(binfile)))
        self._error_check(errcode)
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
        errcode = self.SWMMlibobj.swmm_start(ctypes.c_bool(SaveOut2rpt))
        self._error_check(errcode)

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
        errcode = self.SWMMlibobj.swmm_end()
        self._error_check(errcode)

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
        elapsed_time = ctypes.c_double()
        self.SWMMlibobj.swmm_step(ctypes.byref(elapsed_time))
        return elapsed_time.value

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

        if not hasattr(self, 'curSimTime'):
            self.curSimTime = 0.0

        ctime = self.curSimTime

        secPday = 3600.0 * 24.0
        advanceDays = advanceSeconds / secPday

        eps = advanceDays * 0.00001

        while self.curSimTime <= ctime + advanceDays - eps:
            elapsed_time = ctypes.c_double()
            self.SWMMlibobj.swmm_step(ctypes.byref(elapsed_time))
            if elapsed_time.value == 0:
                return 0.0
            self.curSimTime = elapsed_time.value
        return elapsed_time.value

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
        errcode = self.SWMMlibobj.swmm_report()
        self._error_check(errcode)

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

        errcode = self.SWMMlibobj.swmm_close()
        self._error_check(errcode)
        self.fileLoaded = False

    def swmm_getVersion(self):
        """
        Retrieves version number of current SWMM engine.

        The format used is xyzzz where x = major version number,
        y = minor version number, and zzz = build number.

        :return: version number of the DLL source code
        :rtype: int
        """
        major = ctypes.create_string_buffer(100)
        minor = ctypes.create_string_buffer(100)
        patch = ctypes.create_string_buffer(100)
        self.SWMMlibobj.swmm_getVersionInfo(
            ctypes.byref(major), ctypes.byref(minor), ctypes.byref(patch))
        ver = [
            major.value.decode("utf-8"), minor.value.decode("utf-8"),
            patch.value.decode("utf-8")
        ]
        return distutils.version.LooseVersion('.'.join(ver))

    def swmm_getMassBalErr(self):
        """
        Get Mass Balance Errors.

        :return: Runoff Error, Flow Routing Error, Quality Error
        :rtype: tuple
        """
        runoffErr = ctypes.c_float()
        flowErr = ctypes.c_float()
        qualErr = ctypes.c_float()

        errcode = self.SWMMlibobj.swmm_getMassBalErr(
            ctypes.byref(runoffErr),
            ctypes.byref(flowErr), ctypes.byref(qualErr))
        self._error_check(errcode)
        return runoffErr.value, flowErr.value, qualErr.value

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
        >>> 2015-11-01 14:00:00
        >>> swmm_model.getSimulationDateTime(SimulationTime.EndDateTime)
        >>> 2015-11-04 00:00:00
        >>> swmm_model.getSimulationDateTime(SimulationTime.ReportStart)
        >>> 2015-11-01 14:00:00
        >>>
        >>> swmm_model.swmm_close()
        """
        _year = ctypes.c_int()
        _month = ctypes.c_int()
        _day = ctypes.c_int()
        _hours = ctypes.c_int()
        _minutes = ctypes.c_int()
        _seconds = ctypes.c_int()

        errcode = self.SWMMlibobj.swmm_getSimulationDateTime(
            ctypes.c_int(timeType),
            ctypes.byref(_year),
            ctypes.byref(_month),
            ctypes.byref(_day),
            ctypes.byref(_hours),
            ctypes.byref(_minutes), ctypes.byref(_seconds))
        self._error_check(errcode)
        return datetime(_year.value, _month.value, _day.value, _hours.value,
                        _minutes.value, _seconds.value)

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
        _year = newDateTime.year
        _month = newDateTime.month
        _day = newDateTime.day
        _hours = newDateTime.hour
        _minutes = newDateTime.minute
        _seconds = newDateTime.second
        errcode = self.SWMMlibobj.swmm_setSimulationDateTime(
            ctypes.c_int(timeType), ctypes.c_int(_year), ctypes.c_int(_month),
            ctypes.c_int(_day), ctypes.c_int(_hours), ctypes.c_int(_minutes),
            ctypes.c_int(_seconds))
        self._error_check(errcode)

    def getSimUnit(self, unittype):
        """
        Get Simulation Units.

        :param int unittype: Simulation Unit Type
        :return: Simulation Unit Type
        :rtype: str

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSimUnit(SimulationUnits.FlowUnits)
        >>> CFS
        >>> swmm_model.swmm_close()
        """
        value = ctypes.c_int()
        errcode = self.SWMMlibobj.swmm_getSimulationUnit(unittype,
                                                         ctypes.byref(value))
        self._error_check(errcode)
        if unittype == tka.SimulationUnits.FlowUnits.value:
            # Temporary Solution (2017-1-2 BEM)
            _flowunitnames = ["CFS", "GPM", "MGD", "CMS", "LPS", "MLD"]
            return _flowunitnames[value.value]
        elif unittype == tka.SimulationUnits.UnitSystem.value:
            # Temporary Solution (2017-1-2 BEM)
            _flowunitnames = ["US", "SI"]
            return _flowunitnames[value.value]

    def getSimOptionSetting(self, settingtype):
        """
        Get Simulation Option Settings.

        :param int settingtype: Analysis Option Setting
        :return: Simulation Analysis option setting
        :rtype: bool

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSimAnalysisSetting(SimAnalysisSettings.AllowPonding)
        >>> False
        >>> swmm_model.swmm_close()
        """
        value = ctypes.c_int()
        errcode = self.SWMMlibobj.swmm_getSimulationAnalysisSetting(
            settingtype, ctypes.byref(value))
        self._error_check(errcode)
        return bool(value.value)

    def getSimAnalysisSetting(self, paramtype):
        """
        Get Simulation Configuration Parameter.

        :param int paramtype: Simulation Parameter Type
        :return: Simulation Analysis Parameter Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSimAnalysisSetting(SimulationParameters.RouteStep)
        >>> 300
        >>> swmm_model.swmm_close()
        """
        value = ctypes.c_double()
        errcode = self.SWMMlibobj.swmm_getSimulationParam(paramtype,
                                                          ctypes.byref(value))
        self._error_check(errcode)
        return value.value

    def getProjectSize(self, objecttype):
        """
        Get Project Size: Number of Objects.

        :param int objecttype: (member variable)
        :return: Object Count
        :rtype: int

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getProjectSize(ObjectType.NODE)
        >>> 10
        >>> swmm_model.swmm_close()
        """
        count = ctypes.c_int()
        errcode = self.SWMMlibobj.swmm_countObjects(objecttype,
                                                    ctypes.byref(count))
        self._error_check(errcode)
        return count.value

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
        >>> "example_id_name"
        >>>
        >>> swmm_model.swmm_close()
        """
        ID = ctypes.create_string_buffer(61)
        errcode = self.SWMMlibobj.swmm_getObjectId(objecttype, index,
                                                   ctypes.byref(ID))
        self._error_check(errcode)
        return ID.value.decode("utf-8")

    def getObjectIDList(self, objecttype):
        """
        Get Object ID list.

        :param int objecttype: (member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getObjectIDList(ObjectType.LINK)
        >>> ['C1:C2', 'C2', 'C3']
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
        C_ID = ctypes.c_char_p(six.b(ID))
        index = ctypes.c_int()
        errcode = self.SWMMlibobj.swmm_project_findObject(objecttype, C_ID, ctypes.byref(index))
        index = index.value
        if index != -1:
            return index
        else:
            raise Exception("ID Does Not Exist")

    def ObjectIDexist(self, objecttype, ID):
        """Check if Object ID Exists. Mostly used as an internal function."""
        C_ID = ctypes.c_char_p(six.b(ID))
        index = ctypes.c_int()
        errcode = self.SWMMlibobj.swmm_project_findObject(objecttype, C_ID, ctypes.byref(index))
        index = index.value
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
        >>> 0
        >>>
        >>> swmm_model.getNodeType('J1') is NodeType.junction
        >>> True
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        Ntype = ctypes.c_int()
        errcode = self.SWMMlibobj.swmm_getNodeType(index, ctypes.byref(Ntype))
        self._error_check(errcode)
        return Ntype.value

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
        >>> 3
        >>>
        >>> swmm_model.getLinkType('C1') is LinkType.weir
        >>> True
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        Ltype = ctypes.c_int()
        errcode = self.SWMMlibobj.swmm_getLinkType(index, ctypes.byref(Ltype))
        self._error_check(errcode)
        return Ltype.value

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
        >>> ('NodeUSID','NodeDSID')
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)

        USNodeIND = ctypes.c_int()
        DSNodeIND = ctypes.c_int()

        errcode = self.SWMMlibobj.swmm_getLinkConnections(
            index, ctypes.byref(USNodeIND), ctypes.byref(DSNodeIND))
        self._error_check(errcode)

        USNodeID = self.getObjectId(tka.ObjectType.NODE.value, USNodeIND.value)
        DSNodeID = self.getObjectId(tka.ObjectType.NODE.value, DSNodeIND.value)

        if self._getLinkDirection(ID) == 1:
            # Return Tuple of Upstream and Downstream Node IDS
            return (USNodeID, DSNodeID)
        # link validations reverse the conduit direction if the slope is < 0
        elif self._getLinkDirection(ID) == -1:
            # Return Tuple of Upstream and Downstream Node IDS
            return (DSNodeID, USNodeID)

    def _getLinkDirection(self, ID):
        """
        Internal Method: returns conduit flow direction.

        :param str index: link ID
        :return: 1 for conduit flow from upstream node to downstream node
        and -1 for conduit flow from downstream node to upstream node
        :rtype: int
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        direction = ctypes.c_byte()
        errcode = self.SWMMlibobj.swmm_getLinkDirection(
            index, ctypes.byref(direction))
        self._error_check(errcode)
        return direction.value

    def getNodeParam(self, ID, parameter):
        """
        Get Node Parameter.

        :param str ID: Node ID
        :param int parameter: Paramter (toolkitapi.NodeParams member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getNodeParam('J2',NodeParams.invertElev )
        >>> 13.392
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        param = ctypes.c_double()
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_getNodeParam(index, parameter,
                                                    ctypes.byref(param))
        self._error_check(errcode)
        return param.value

    def setNodeParam(self, ID, parameter, value):
        """
        Set Node Parameter.

        :param str ID: Node ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getNodeParam('J2',NodeParams.invertElev, 19 )
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        _val = ctypes.c_double(value)
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_setNodeParam(index, parameter, _val)
        self._error_check(errcode)

    def getLinkParam(self, ID, parameter):
        """
        Get Link Parameter.

        :param str ID: Link ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLinkParam('C1:C2',LinkParams.offset1 )
        >>> 0.0
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        param = ctypes.c_double()
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_getLinkParam(index, parameter,
                                                    ctypes.byref(param))
        self._error_check(errcode)
        return param.value

    def setLinkParam(self, ID, parameter, value):
        """
        Set Link Parameter.

        :param str ID: Link ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLinkParam('C1:C2',LinkParams.offset1, 2 )
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        _val = ctypes.c_double(value)
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_setLinkParam(index, parameter, _val)
        self._error_check(errcode)
        
    def getLidCOverflow(self, ID):
        """
        Get Lid Control Parameter.

        :param str ID: Lid Control ID
        :rtype: Bool

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLidCOverflow('J2')
        >>> True
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LID.value, ID)
        param = ctypes.c_char()
        errcode = self.SWMMlibobj.swmm_getLidCOverflow(index,
                                                       ctypes.byref(param))
        self._error_check(errcode)
        if param.value == struct.pack('B', 0): return False
        else: return True

    def setLidCOverflow(self, ID, value):
        """
        Set Lid Control Parameter.

        :param str ID: Lid Control ID

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLidCOverflow('J2', False)
        >>>
        >>> swmm_model.swmm_close()
        """
        _val = ctypes.c_char(value)
        index = self.getObjectIDIndex(tka.ObjectType.LID.value, ID)
        errcode = self.SWMMlibobj.swmm_setLidCOverflow(index,
                                                       _val)
        self._error_check(errcode)

    def getLidCParam(self, ID, layer, parameter):
        """
        Get LidControl Parameter.

        :param str ID: Lid Control ID
        :param int layer: Layer (toolkitapi.LidLayers member variable)
        :param int parameter: Paramter (toolkitapi.LidLayersProperty member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLidCParam('J2', LidLayer.surface, LidLayersProperty.thickness)
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LID.value, ID)
        param = ctypes.c_double()
        if not isinstance(layer, int):
            layer = layer.value
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_getLidCParam(index,
                                                    layer,
                                                    parameter,
                                                    ctypes.byref(param))
        self._error_check(errcode)
        return param.value

    def setLidCParam(self, sim_start, ID, layer, parameter, value):
        """
        Set Lid Control Parameter Before/During Model Simulation.

        :param str ID: Lid Control ID
        :param int layer: Layer (toolkitapi.LidLayers member variable)
        :param int parameter: Paramter (toolkitapi.LidLayersProperty member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLidCParam('J2', LidLayer.surface, LidLayersProperty.thickness, 110)

        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LID.value, ID)
        _val = ctypes.c_double(value)
        if not isinstance(layer, int):
            layer = layer.value
        if not isinstance(parameter, int):
            parameter = parameter.value

        if not sim_start:
            errcode = self.SWMMlibobj.swmm_setLidCParamBeforeSimulation(index,
                                                                        layer,
                                                                        parameter,
                                                                        _val)
        else:
            errcode = self.SWMMlibobj.swmm_setLidCParamDuringSimulation(index,
                                                                        layer,
                                                                        parameter,
                                                                        _val)

        self._error_check(errcode)

    def setLidCParamDuringimulation(self, ID, layer, parameter, value):
        """
        Set Lid Control Parameter During Model Simulation.

        :param str ID: Lid Control ID
        :param int layer: Layer (toolkitapi.LidLayers member variable)
        :param int parameter: Paramter (toolkitapi.LidLayersProperty member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLidCParam('J2', LidLayer.surface, LidLayersProperty.thickness, 110)

        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LID.value, ID)
        _val = ctypes.c_double(value)
        if not isinstance(layer, int):
            layer = layer.value
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_setLidCParamDuringSimulation(index,
                                                                    layer,
                                                                    parameter,
                                                                    _val)
        
    def getLidUCount(self, ID):
        """
        Get Number of Lid Units Defined for Subcatchment.

        :param str ID: Subcatchment ID
        :rtype: int

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLidUCount('J2')
        >>> 2
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        param = ctypes.c_int()
        errcode = self.SWMMlibobj.swmm_getLidUCount(index,
                                                    ctypes.byref(param))
        self._error_check(errcode)
        return param.value
        
    def getLidUParam(self, subcatchID, lidIndex, parameter):
        """
        Get LidUnit Parameter

        :param str subcatchID: Subcatchment ID
        :param int lidID: Lid unit Index
        :param int Parameter: Paramter (toolkitapi.LidUParams member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLidUParam('S2', 0, LidUParams.unitarea)
        >>> 1000
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        param = ctypes.c_double()
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_getLidUParam(index,
                                                    lidIndex,
                                                    parameter,
                                                    ctypes.byref(param))
        self._error_check(errcode)
        return param.value

    def setLidUParam(self, subcatchID, lidIndex, parameter, value):
        """
        Set LidUnit Parameter

        :param str subcatchID: Subcatchment ID
        :param int lidID: Lid unit Index
        :param int Parameter: Paramter (toolkitapi.LidUParams member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLidUParam('S2', 0, LidUParams.unitarea, 10)
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        _val = ctypes.c_double(value)
        param = ctypes.c_double()
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_setLidUParam(index,
                                                    lidIndex,
                                                    parameter,
                                                    _val)
        
    def getLidUOption(self, subcatchID, lidIndex, parameter):
        """
        Get LidUnit Option

        :param str subcatchID: Subcatchment ID
        :param int lidID: Lid unit Index
        :param int Parameter: Paramter (toolkitapi.LidUParams member variable)
        :return: Paramater Value
        :rtype: int

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLidUOption('S2', 0, LidUParams.index)
        >>> 1000
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        param = ctypes.c_int()
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_getLidUOption(index,
                                                     lidIndex,
                                                     parameter,
                                                     ctypes.byref(param))
        self._error_check(errcode)
        return param.value

    def setLidUOption(self, subcatchID, lidIndex, parameter, value):
        """
        Set LidUnit Option

        :param str subcatchID: Subcatchment ID
        :param int lidID: Lid unit Index
        :param int Parameter: Paramter (toolkitapi.LidUParams member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLidUOption('S2', 0, LidUParams.index, 0)
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        _val = ctypes.c_int(value)
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_setLidUOption(index,
                                                     lidIndex,
                                                     parameter,
                                                     _val)
        self._error_check(errcode)
    
    def getSubcatchParam(self, ID, parameter):
        """
        Get Subcatchment Parameter

        :param str ID: Subcatchment ID
        :param int Parameter: Paramter (toolkitapi.SubcParams member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLinkParam('S2',SubcParams.area )
        >>> 43561.596096880996
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        param = ctypes.c_double()
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_getSubcatchParam(index, parameter,
                                                        ctypes.byref(param))
        self._error_check(errcode)
        return param.value

    def setSubcatchParam(self, ID, parameter, value):
        """
        Set Subcatchment Parameter.

        :param str ID: Subcatchment ID
        :param int Parameter: Paramter (toolkitapi.SubcParams member variable)

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLinkParam('S2',SubcParams.area, 100 )
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        _val = ctypes.c_double(value)
        if not isinstance(parameter, int):
            parameter = parameter.value
        errcode = self.SWMMlibobj.swmm_setSubcatchParam(index, parameter, _val)
        self._error_check(errcode)

    def getSubcatchOutConnection(self, ID):
        """
        Get Subcatchment Outlet Connection.

        This function return the type of loading surface and the ID. The two
        load to objects are nodes and other subcatchments.

        Nodes are ObjectType.NODE
        Subcatchments are ObjectType.SUBCATCH

        :param str ID: Subcatchment ID
        :param int Parameter: Paramter (toolkitapi.SubcParams member variable)
        :return: (Loading Surface Type, ID)
        :rtype: tuple

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSubcatchOutConnection('S2',SubcParams.area )
        >>> (2, 'J2')
        >>>
        >>> subout = swmm_model.getSubcatchOutConnection('S2',SubcParams.area )
        >>> subout[0]  == ObjectType.NODE
        >>> True
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        TYPELoadSurface = ctypes.c_int()
        outindex = ctypes.c_int()
        errcode = self.SWMMlibobj.swmm_getSubcatchOutConnection(
            index, ctypes.byref(TYPELoadSurface), ctypes.byref(outindex))
        self._error_check(errcode)

        if TYPELoadSurface.value == tka.ObjectType.NODE.value:
            LoadID = self.getObjectId(tka.ObjectType.NODE.value,
                                      outindex.value)

        if TYPELoadSurface.value == tka.ObjectType.SUBCATCH.value:
            LoadID = self.getObjectId(tka.ObjectType.SUBCATCH.value,
                                      outindex.value)

        return (TYPELoadSurface.value, LoadID)

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
        ...     print swmm_model.getCurrentSimualationTime()
        ...     if (time <= 0.0): break
        ...
        >>> 2015-11-03 10:10:12
        >>> 2015-11-03 10:20:12
        >>> 2015-11-03 10:30:12
        >>> 2015-11-03 10:40:12
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        _year = ctypes.c_int()
        _month = ctypes.c_int()
        _day = ctypes.c_int()
        _hours = ctypes.c_int()
        _minutes = ctypes.c_int()
        _seconds = ctypes.c_int()
        errcode = self.SWMMlibobj.swmm_getCurrentDateTime(ctypes.byref(_year),
                                                          ctypes.byref(_month),
                                                          ctypes.byref(_day),
                                                          ctypes.byref(_hours),
                                                          ctypes.byref(_minutes),
                                                          ctypes.byref(_seconds))
        self._error_check(errcode)
        if errcode == 0:
            return datetime(_year.value, _month.value, _day.value, _hours.value,
                            _minutes.value, _seconds.value)

    def getLidUFluxRates(self, subcatchID, lidIndex, layerIndex):
        """
        Get Lid Unit Layer Flux Rates Result.

        :param str subcatchID: Subcatchment ID
        :param int lidIndex: Lid unit Index
        :param int layerIndex: Paramter (toolkitapi.LidLayers member variable)
        :return: Paramater Value
        :rtype: float
        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print swmm_model.getLidUFluxRates('J1', 0, LidLayers.surface)
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        result = ctypes.c_double()
        if not isinstance(layerIndex, int):
            layerIndex = layerIndex.value
        errcode = self.SWMMlibobj.swmm_getLidUFluxRates(index,
                                                        lidIndex,
                                                        layerIndex,
                                                        ctypes.byref(result))
        self._error_check(errcode)
        return result.value

    def getLidUResult(self, subcatchID, lidIndex, resultType):
        """
        Get Lid Result.

        :param str subcatchID: Subcatchment ID
        :param int lidIndex: Lid unit Index
        :param int resultType: Paramter (toolkitapi.LidUResults member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print swmm_model.getLidUResult('J1', 0, LidUResults.inflow)
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        result = ctypes.c_double()
        if not isinstance(resultType, int):
            resultType = resultType.value
        errcode = self.SWMMlibobj.swmm_getLidUResult(index,
                                                     lidIndex,
                                                     resultType,
                                                     ctypes.byref(result))
        self._error_check(errcode)
        return result.value

    def getLidGResult(self, subcatchID, resultType):
        """
        Get Lid Group Result.

        :param str subcatchID: Subcatchment ID
        :param int resultType: Paramter (toolkitapi.LidUResults member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print swmm_model.getLidGResult('J1', LidUResults.flowToPerv)
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, subcatchID)
        result = ctypes.c_double()
        errcode = self.SWMMlibobj.swmm_getLidGResult(index,
                                                     resultType,
                                                     ctypes.byref(result))
        self._error_check(errcode)
        return result.value
    
    def getNodeResult(self, ID, resultType):
        """
        Get Node Result.

        :param str ID: Node ID
        :param int Parameter: Paramter (toolkitapi.NodeResults member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print swmm_model.getNodeResult('J1', NodeResults.newDepth)
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        result = ctypes.c_double()
        errcode = self.SWMMlibobj.swmm_getNodeResult(index, resultType,
                                                     ctypes.byref(result))
        self._error_check(errcode)
        return result.value

    def getLinkResult(self, ID, resultType):
        """
        Get Link Result.

        :param str ID: Link ID
        :param int Parameter: Paramter (toolkitapi.LinkResults member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print swmm_model.getLinkResult('J1', LinkResults.newFlow)
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)
        result = ctypes.c_double()
        errcode = self.SWMMlibobj.swmm_getLinkResult(index, resultType,
                                                     ctypes.byref(result))
        self._error_check(errcode)
        return result.value

    def getSubcatchResult(self, ID, resultType):
        """
        Get Subcatchment Result

        :param str ID: Subcatchment ID
        :param int Parameter: Paramter (toolkitapi.LinkResults member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print swmm_model.getSubcatchResult('S3', SubcResults.newRunoff)
        ...     if (time <= 0.0): break
        ...
        >>> 0.01
        >>> 0.05
        >>> 0.09
        >>> 0.08
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)
        result = ctypes.c_double()
        errcode = self.SWMMlibobj.swmm_getSubcatchResult(index, resultType,
                                                         ctypes.byref(result))
        self._error_check(errcode)

        return result.value
    
    def getSubcatchPollut(self, ID, resultType):
        """
        Get pollutant results from a Subcatchment.

        :param str ID: Subcatchment ID
        :param int Parameter: Parameter (toolkitapi.SubcPollut member variable)
        :return: Pollutant Values
        :rtype: list
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)

        pollut_ids = self.getObjectIDList(tka.ObjectType.POLLUT.value)        
        result = ctypes.POINTER(ctypes.c_double * len(pollut_ids))()
        pollut_values = []
        errcode = self.SWMMlibobj.swmm_getSubcatchPollut(index, resultType,
                                                         ctypes.byref(result))

        for ind in range(len(pollut_ids)):
            value = ctypes.cast(result, ctypes.POINTER(ctypes.c_double))[ind]
            pollut_values.append(value)

        self._error_check(errcode)

        freeresultarray = self.SWMMlibobj.freeArray
        freeresultarray(ctypes.byref(result))

        return pollut_values

    def node_statistics(self, ID):
        """
        Get stats for a Node.

        :param str ID: Node ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)

        # SWMM function handle.
        swmm_stats_func = self.SWMMlibobj.swmm_getNodeStats
        # SWMM function handle argument output structure.
        swmm_stats_func_arg = ctypes.POINTER(tka.NodeStats)
        # Define argument.
        swmm_stats_func.argtypes = (
            ctypes.c_int,
            swmm_stats_func_arg, )

        object_stats = tka.NodeStats()
        errcode = swmm_stats_func(
            ctypes.c_int(index), ctypes.byref(object_stats))

        self._error_check(errcode)
        # Copy Items to Dictionary using Alias Names.
        out_dict = {}
        for attr in dir(object_stats):
            if "_" not in attr:
                out_dict[object_stats._py_alias_ids[attr]] = getattr(
                    object_stats, attr)
        return out_dict

    def node_inflow(self, ID):
        """
        Get total inflow volume for a Node.

        :param str ID: Node ID
        :return: Total Volume
        :rtype: float
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)
        result = ctypes.c_double()
        errcode = self.SWMMlibobj.swmm_getNodeTotalInflow(index,
                                                          ctypes.byref(result))
        self._error_check(errcode)
        return result.value

    def storage_statistics(self, ID):
        """
        Get stats for a Storage Node.

        :param str ID: Node ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)

        # SWMM function handle.
        swmm_stats_func = self.SWMMlibobj.swmm_getStorageStats
        # SWMM function handle argument output structure.
        swmm_stats_func_arg = ctypes.POINTER(tka.StorageStats)
        # Define argument.
        swmm_stats_func.argtypes = (
            ctypes.c_int,
            swmm_stats_func_arg, )

        object_stats = tka.StorageStats()
        errcode = swmm_stats_func(
            ctypes.c_int(index), ctypes.byref(object_stats))

        self._error_check(errcode)
        # Copy Items to Dictionary using Alias Names.
        out_dict = {}
        for attr in dir(object_stats):
            if "_" not in attr:
                out_dict[object_stats._py_alias_ids[attr]] = getattr(
                    object_stats, attr)
        return out_dict

    def outfall_statistics(self, ID):
        """
        Get stats for a Outfall Node.

        :param str ID: Node ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.NODE.value, ID)

        # SWMM function handle.
        swmm_stats_func = self.SWMMlibobj.swmm_getOutfallStats
        # SWMM function handle argument output structure.
        swmm_stats_func_arg = ctypes.POINTER(tka.OutfallStats)
        # Define argument.
        swmm_stats_func.argtypes = (
            ctypes.c_int,
            swmm_stats_func_arg, )

        object_stats = tka.OutfallStats()
        errcode = swmm_stats_func(
            ctypes.c_int(index), ctypes.byref(object_stats))

        self._error_check(errcode)
        # Copy Items to Dictionary using Alias Names.
        out_dict = {}
        for attr in dir(object_stats):
            if "_" not in attr:
                # Pollutant Array.
                if attr == "totalLoad":
                    out_dict[object_stats._py_alias_ids[attr]] = {}
                    pol_stats_array = getattr(object_stats, attr)
                    pollut_ids = self.getObjectIDList(
                        tka.ObjectType.POLLUT.value)
                    if len(pollut_ids) > 0:
                        for ind in range(len(pollut_ids)):
                            out_dict[object_stats._py_alias_ids[attr]][
                                pollut_ids[ind]] = pol_stats_array[ind]
                else:
                    out_dict[object_stats._py_alias_ids[attr]] = getattr(
                        object_stats, attr)

        # Free Outfall Stats Pollutant Array.
        freeoutfallstats = self.SWMMlibobj.swmm_freeOutfallStats
        freeoutfallstats.argtypes = (swmm_stats_func_arg, )
        freeoutfallstats(object_stats)

        return out_dict

    def conduit_statistics(self, ID):
        """
        Get stats for a Conduits.

        :param str ID: Conduit ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)

        # SWMM function handle.
        swmm_stats_func = self.SWMMlibobj.swmm_getLinkStats
        # SWMM function handle argument output structure.
        swmm_stats_func_arg = ctypes.POINTER(tka.LinkStats)
        # Define argument.
        swmm_stats_func.argtypes = (
            ctypes.c_int,
            swmm_stats_func_arg, )

        object_stats = tka.LinkStats()
        errcode = swmm_stats_func(
            ctypes.c_int(index), ctypes.byref(object_stats))

        self._error_check(errcode)
        # Copy Items to Dictionary using Alias Names.
        out_dict = {}
        for attr in dir(object_stats):
            if "_" not in attr:
                # Pollutant Array
                if attr == "timeInFlowClass":
                    out_dict[object_stats._py_alias_ids[attr]] = {}
                    stats_array = getattr(object_stats, attr)
                    sum_array = sum([val for val in stats_array])
                    for ind in range(7):
                        out_dict[object_stats._py_alias_ids[attr]][
                            ind] = stats_array[ind] / sum_array
                else:
                    out_dict[object_stats._py_alias_ids[attr]] = getattr(
                        object_stats, attr)

        return out_dict

    def pump_statistics(self, ID):
        """
        Get stats for a Pump.

        :param str ID: Pump ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.LINK.value, ID)

        # SWMM function handle.
        swmm_stats_func = self.SWMMlibobj.swmm_getPumpStats
        # SWMM function handle argument output structure.
        swmm_stats_func_arg = ctypes.POINTER(tka.PumpStats)
        # Define argument.
        swmm_stats_func.argtypes = (
            ctypes.c_int,
            swmm_stats_func_arg, )

        object_stats = tka.PumpStats()
        errcode = swmm_stats_func(
            ctypes.c_int(index), ctypes.byref(object_stats))

        self._error_check(errcode)
        # Copy Items to Dictionary using Alias Names.
        out_dict = {}
        for attr in dir(object_stats):
            if "_" not in attr:
                out_dict[object_stats._py_alias_ids[attr]] = getattr(
                    object_stats, attr)
                if attr == "utilized":
                    out_dict[object_stats._py_alias_ids[attr]] = getattr(
                        object_stats, attr) / object_stats.totalPeriods
        return out_dict

    def subcatch_statistics(self, ID):
        """
        Get stats for a Subcatchment.

        :param str ID: Subcatchment ID
        :return: Group Stats
        :rtype: dict
        """
        index = self.getObjectIDIndex(tka.ObjectType.SUBCATCH.value, ID)

        # SWMM function handle.
        swmm_stats_func = self.SWMMlibobj.swmm_getSubcatchStats
        # SWMM function handle argument output structure.
        swmm_stats_func_arg = ctypes.POINTER(tka.SubcStats)
        # Define argument.
        swmm_stats_func.argtypes = (
            ctypes.c_int,
            swmm_stats_func_arg, )

        object_stats = tka.SubcStats()
        errcode = swmm_stats_func(
            ctypes.c_int(index), ctypes.byref(object_stats))

        self._error_check(errcode)
        # Copy Items to Dictionary using Alias Names.
        out_dict = {}
        for attr in dir(object_stats):
            if "_" not in attr:
                out_dict[object_stats._py_alias_ids[attr]] = getattr(
                    object_stats, attr)


        return out_dict

    def flow_routing_stats(self):
        """
        Get Flow Routing System stats.

        :return: Dictionary of Flow Routing Stats.
        :rtype: dict
        """
        # SWMM function handle.
        swmm_stats_func = self.SWMMlibobj.swmm_getSystemRoutingStats
        # SWMM function handle argument output structure.
        swmm_stats_func_arg = ctypes.POINTER(tka.RoutingTotals)
        # Define argument.
        swmm_stats_func.argtypes = (swmm_stats_func_arg, )

        object_stats = tka.RoutingTotals()
        errcode = swmm_stats_func(ctypes.byref(object_stats))

        self._error_check(errcode)

        # Copy Items to Dictionary using Alias Names.
        out_dict = {}
        for attr in dir(object_stats):
            if "_" not in attr:
                out_dict[object_stats._py_alias_ids[attr]] = getattr(
                    object_stats, attr)
        return out_dict

    def runoff_routing_stats(self):
        """
        Get Runoff Routing System stats.

        :return: Dictionary of Runoff Routing Stats.
        :rtype: dict
        """
        # SWMM function handle.
        swmm_stats_func = self.SWMMlibobj.swmm_getSystemRunoffStats
        # SWMM function handle argument output structure.
        swmm_stats_func_arg = ctypes.POINTER(tka.RunoffTotals)
        # Define argument.
        swmm_stats_func.argtypes = (swmm_stats_func_arg, )

        object_stats = tka.RunoffTotals()
        errcode = swmm_stats_func(ctypes.byref(object_stats))

        self._error_check(errcode)

        # Copy Items to Dictionary using Alias Names.
        out_dict = {}
        for attr in dir(object_stats):
            if "_" not in attr:
                out_dict[object_stats._py_alias_ids[attr]] = getattr(
                    object_stats, attr)
        return out_dict

    # --- Active Simulation Parameter "Setters"
    # -------------------------------------------------------------------------
    def setLinkSetting(self, ID, targetSetting):
        """
        Set Link Setting (Pumps, Orifices, Weirs).

        :param str ID: Link ID
        :param float targetSetting: New target setting which will be applied
        at the start of the next routing step.

        Examples:

        >>> swmm_model = PySWMM(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_start()
        >>> i = 0
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     i+=1
        ...
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
        targetSetting = ctypes.c_double(targetSetting)
        errcode = self.SWMMlibobj.swmm_setLinkSetting(index, targetSetting)
        self._error_check(errcode)

    def setNodeInflow(self, ID, flowrate):
        """
        Set Node Inflow rate.

        The flow rate should be in the user defined units. The value is held
        constant in the model until it is redefined by the toolkit API.

        :param str ID: Node ID
        :param float flowrate: New flow rate in the user-defined flow units

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
        q = ctypes.c_double(flowrate)
        errcode = self.SWMMlibobj.swmm_setNodeInflow(index, q)
        self._error_check(errcode)

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
        q = ctypes.c_double(stage)
        errcode = self.SWMMlibobj.swmm_setOutfallStage(index, q)
        self._error_check(errcode)


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
