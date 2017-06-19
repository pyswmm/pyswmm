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

# Third party imports
import six

# Local imports
from pyswmm.lib import DLL_SELECTION
import pyswmm.toolkitapi as tka

# Local variables
SWMM_VER_51011 = '5.1.11'


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

    def __init__(self, inpfile='', rptfile=None, binfile=None):
        """
        Initialize the PySWMM object class.

        :param str inpfile: Name of SWMM input file (default '')
        :param str rptfile: Report file to generate (default None)
        :param str binfile: Optional binary output file (default None)
        """
        self.fileLoaded = False
        self.inpfile = inpfile
        self.rptfile = rptfile
        self.binfile = binfile

        if os.name == 'nt':
            # Windows Support
            self.SWMMlibobj = ctypes.WinDLL(DLL_SELECTION())

        if sys.platform == 'darwin':
            # Mac Osx Support
            self.SWMMlibobj = ctypes.cdll.LoadLibrary(DLL_SELECTION())

        if sys.platform.startswith('linux'):
            # Linux Support
            self.SWMMlibobj = ctypes.CDLL(DLL_SELECTION())

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
        Checks SWMM Error Message and raises Exception or warning.

        :param int errcode: SWMM error code index
        """
        if errcode != 0 and errcode <= 103:
            raise SWMMException(errcode, self._error_message(errcode))

        if errcode != 0 and errcode > 103:
            warnings.warn(self._error_message(errcode))

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
        except:
            PYSWMMException("Run Failed")
        finally:
            try:
                self.swmm_close()
                sys.stdout.write("\n... Closed")
                sys.stdout.write("\n\n... SWMM completed.\n")
            except:
                PYSWMMException("SWMM Close Failed")
                sys.stdout.write("\n\n... SWMM completed. There are errors.\n")

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
            ctypes.c_char_p(inpfile),
            ctypes.c_char_p(rptfile), ctypes.c_char_p(binfile))

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

        if binfile is None:
            if self.binfile != '' and self.binfile is not None:
                binfile = self.binfile
            else:
                binfile = self.inpfile.replace('.inp', '.out')

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
        Produces SWMM Report (*.rpt) file after simulation.

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
        version = str(self.SWMMlibobj.swmm_getVersion())
        major = version[0]
        minor = version[1]
        build = str(int(version[2:]))
        ver = [major, minor, build]
        return distutils.version.StrictVersion('.'.join(ver))

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
        dtme = ctypes.create_string_buffer(61)
        errcode = self.SWMMlibobj.swmm_getSimulationDateTime(
            ctypes.c_int(timeType), dtme)
        self._error_check(errcode)
        if self.swmm_getVersion() < distutils.version.StrictVersion(
                SWMM_VER_51011):
            return datetime.strptime(
                dtme.value.decode("utf-8"), "%b-%d-%Y %H:%M:%S")
        else:
            return datetime.strptime(
                dtme.value.decode("utf-8"), "%m/%d/%Y %H:%M:%S")

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
        dtme = ctypes.create_string_buffer(
            six.b(newDateTime.strftime("%m/%d/%Y %H:%M:%S")))
        errcode = self.SWMMlibobj.swmm_setSimulationDateTime(
            ctypes.c_int(timeType), dtme)
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
        index = self.SWMMlibobj.project_findObject(objecttype, C_ID)
        if index != -1:
            return index
        else:
            raise Exception("ID Does Not Exist")

    def ObjectIDexist(self, objecttype, ID):
        """Check if Object ID Exists. Mostly used as an internal function."""
        C_ID = ctypes.c_char_p(six.b(ID))
        index = self.SWMMlibobj.project_findObject(objecttype, C_ID)
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
        dtme = ctypes.create_string_buffer(61)
        errcode = self.SWMMlibobj.swmm_getCurrentDateTimeStr(dtme)
        self._error_check(errcode)
        if errcode == 0:
            if self.swmm_getVersion() < distutils.version.StrictVersion(
                    SWMM_VER_51011):
                return datetime.strptime(
                    dtme.value.decode("utf-8"), "%b-%d-%Y %H:%M:%S")
            else:
                return datetime.strptime(
                    dtme.value.decode("utf-8"), "%m/%d/%Y %H:%M:%S")

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

    def system_flow_routing(self, resultType):
        """
        Get Cumulative System Flow Routing Stats.

        :param int resultType: Results Type based on SysRoutingStats
        """
        result = ctypes.c_double()
        errcode = self.SWMMlibobj.swmm_getSystemRoutingTotals(
            resultType, ctypes.byref(result))

        self._error_check(errcode)

        return result.value

    def system_runoff_routing(self, resultType):
        """
        Get Cumulative System Runoff Routing Stats.

        :param int resultType: Results Type based on SysRunoffStats
        """
        result = ctypes.c_double()
        errcode = self.SWMMlibobj.swmm_getSystemRunoffTotals(
            resultType, ctypes.byref(result))

        self._error_check(errcode)

        return result.value

    # --- Active Simulation Parameter "Setters"
    # -------------------------------------------------------------------------
    def setLinkSetting(self, ID, targetSetting):
        """
        Set Link Setting (Pumps, Orifices, Weirs).

        :param str ID: Link ID
        :param float targetSetting: New target setting which will be applied
        at the start of the next routing step

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

        The flow rate should be in the user defined units. The value is help
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

    test.swmm_close()
