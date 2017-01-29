"""
Python extensions for the SWMM5 Programmers toolkit

Open Water Analytics (http://wateranalytics.org/)

Author: Bryant E. McDonnell (EmNet LLC)

Last Update: 11/10/2016 

"""


import os
import sys
from datetime import datetime
import warnings

from ctypes import byref, c_double, c_float, c_int, c_char_p, create_string_buffer, c_byte, c_bool

from toolkitapi import *

__author__ = 'Bryant E. McDonnell (EmNet LLC) - bemcdonnell@gmail.com'
__copyright__ = 'Copyright (c) 2016 Bryant E. McDonnell'
__licence__ = 'BSD2'
__version__ = '0.2.1'

class SWMMException(Exception):
    """
    Custom exception class for SWMM errors.
    """
    def __init__(self, error_code, error_message):
        self.warning = False
        self.args = (error_code,)
        self.message = error_message
    def __str__(self):
        return self.message

class PYSWMMException(Exception):
    """
    Custom exception class for PySWMM errors.
    """
    def __init__(self, error_message):
        self.warning = False
        self.message = error_message
    def __str__(self):
        return self.message
    
class pyswmm(object):
    """
    Wrapper class to lead SWMM DLL object, then perform operations on
    the SWMM object that is created when the file is being loaded.

    PySWMM can be run in two different modes:
    
    Mode 1: Execute simulation without any intervention 
    
    * Open the Input file using swmm_open()
    * Execute the simlation without intervening swmmExec()
    * then close calling swmm_close()
    
    Examples:

    >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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

    >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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


    def __init__(self, inpfile = '', rptfile = '', binfile ='', dllpath = None):
        """
        Initialize the pyswmm object class

        :param str inpfile: Name of SWMM input file (default '')
        :param str rptfile: Report file to generate (default '')
        :param str binfile: Optional binary output file (default '')
        """
        self.fileLoaded = False
        self.inpfile = inpfile
        self.rptfile = rptfile
        self.binfile = binfile

        def get_pkgpath():
            # Dynamically finds path to SWMM linking library
            import toolkitapi as tkp
            return os.path.dirname(tkp.__file__.replace('\\','/'))
        
        # The following should be un commented if using on mac
        #### darwin
        #if 'darwin' in sys.platform:
        #    from ctypes import cdll
        #    libpath = os.getcwd()
        #    libswmm = '/pyswmm/swmmLinkedLibs/Darwin/libswmm.dylib'
        #    self.SWMMlibobj = cdll.LoadLibrary(libpath+libswmm)

        #### windows
        if 'win32' in sys.platform:
            from ctypes import CDLL
            if dllpath == None:
                dllname = 'swmm5.dll'
                libswmm = get_pkgpath() + '\\swmmLinkedLibs\\Windows\\' + dllname
            else:
                libswmm = dllpath
            self.SWMMlibobj = CDLL(libswmm)
##            self.SWMMlibobj = windll.LoadLibrary(libswmm)
            

    def _error_message(self, errcode):
        """
        Returns SWMM Error Message

        :param int errcode: SWMM error code index
        :return: Error Message from SWMM
        :rtype: str
        
        """
        errcode = c_int(errcode)
        _errmsg = create_string_buffer(257)
        self.SWMMlibobj.swmm_getError(errcode, _errmsg)
        return _errmsg.value
            
    def _error_check(self, errcode):
        """
        Checks SWMM Error Message and raises Exception or warning

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

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmmExec()
        >>> swmm_model.swmm_close()        
        """
        
        if inpfile is None:
            inpfile = self.inpfile
        if rptfile is None:
            if self.rptfile != '': rptfile = self.rptfile
            else: rptfile = self.inpfile.replace('.inp','.rpt')
        if binfile is None:
            if self.binfile != '': binfile = self.binfile
            else: binfile = self.inpfile.replace('.inp','.rpt') 
        sys.stdout.write("\n... SWMM Version {}".format(self.swmm_getVersion()))

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
            
    def swmm_run(self,inpfile=None, rptfile=None,binfile = None):
        if inpfile is None: inpfile = self.inpfile
        if rptfile is None:
            if self.rptfile != '': rptfile = self.rptfile
            else: rptfile = self.inpfile.replace('.inp','.rpt')
        if binfile is None:
            if self.binfile != '': binfile = self.binfile
            else: binfile = self.inpfile.replace('.inp','.out') 

        self.SWMMlibobj.swmm_run(c_char_p(inpfile), c_char_p(rptfile), c_char_p(binfile))
        
    def swmm_open(self, inpfile=None, rptfile=None, binfile=None):
        """
        Opens SWMM input file & reads in network data
        
        :param str inpfile: Name of SWMM input file
        :param str rptfile: Report file to generate
        :param str binfile: Optional binary output file

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_close()          
        """
        if self.fileLoaded:
            self.swmm_close()
            raise(PYSWMMException('Fatal error closing previously opened file'))
        if inpfile is None:
            inpfile = self.inpfile
        if rptfile is None:
            if self.rptfile != '': rptfile = self.rptfile
            else: rptfile = self.inpfile.replace('.inp','.rpt')
        if binfile is None:
            if self.binfile != '': binfile = self.binfile
            else: binfile = self.inpfile.replace('.inp','.out')            

        errcode = self.SWMMlibobj.swmm_open(c_char_p(inpfile),\
                                            c_char_p(rptfile),\
                                            c_char_p(binfile))
        self._error_check(errcode)
        self.fileLoaded = True
        
    def swmm_start(self, SaveOut2rpt = False):
        """Prepares to Start SWMM Simulation

        :param bool SaveOut2rpt: Save timeseries results to rpt file (default is False).

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        
        errcode = self.SWMMlibobj.swmm_start(c_bool(SaveOut2rpt))
        self._error_check(errcode)
        
    def swmm_end(self):
        """Ends SWMM Simulation

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        """ Advances SWMM Simulation by a single routing step

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        elapsed_time = c_double()
        self.SWMMlibobj.swmm_step(byref(elapsed_time))

        return elapsed_time.value

    def swmm_stride(self, advanceSeconds):
        """This function allows for user defined stride length to advance
        the model simulation by a defined time.  This is useful when control
        rules are managed externally by PySWMM. Instead of evaluating rules
        every routing step, instead the simulation can be advanced further
        in time before the PySWMM can intervene. When a 0 is returned, the
        simulation period has reached the end.

        :param int advanceSeconds: Number seconds to advance the simulation forward.
        :return: Current simulation time after a stride in decimal days (float)
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> while(True):
        ...     time = swmm_model.swmm_stride(600)
        ...     if (time <= 0.0): break
        >>>
        >>> swmm_model.swmm_end()
        >>> swmm_model.swmm_report()
        >>> swmm_model.swmm_close()        
        """
        if not hasattr(self, 'curSimTime'): self.curSimTime = 0.000001
        
        ctime = self.curSimTime
        while advanceSeconds/3600./24. + ctime > self.curSimTime:
            elapsed_time = c_double()
            self.SWMMlibobj.swmm_step(byref(elapsed_time))
            self.curSimTime = elapsed_time.value
            if elapsed_time.value == 0:
                return 0.0

        return elapsed_time.value
        
    def swmm_report(self):
        """ Produces SWMM Report (*.rpt) file after simulation

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        """ Closes model and supporting files and cleans up memory

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        retrieves version number of current SWMM engine which
        uses a format of xyzzz where x = major version number,
        y = minor version number, and zzz = build number.
        
        :return: version number of the DLL source code
        :rtype: int
        
        """
        return self.SWMMlibobj.swmm_getVersion()

    def swmm_getMassBalErr(self):
        """ Get Mass Balance Errors

        :return: Runoff Error, Flow Routing Error, Quality Error
        :rtype: tuple
        
        """
        runoffErr = c_float()
        flowErr = c_float()
        qualErr = c_float()

        errcode = self.SWMMlibobj.swmm_getMassBalErr(byref(runoffErr),\
                                                          byref(flowErr),\
                                                          byref(qualErr))
        self._error_check(errcode)
        
        return runoffErr.value, flowErr.value, qualErr.value

    #### NETWORK API FUNCTIONS
    def getSimulationDateTime(self, timeType):
        """
        Get Simulation Time Data (Based on SimulationTime options)

        :param int timeType: (toolkitapi.SimulationTime member variable)
        :return: datetime
        :rtype: datetime

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        dtme = create_string_buffer(61)

        errcode = self.SWMMlibobj.swmm_getSimulationDateTime(c_int(timeType), dtme)
        self._error_check(errcode)
        
        return datetime.strptime(dtme.value, "%b-%d-%Y %H:%M:%S")

    def setSimulationDateTime(self, timeType, newDateTime):
        """
        Set Simulation Time Data (Based on SimulationTime options)

        :param int timeType: (toolkitapi.SimulationTime member variable)

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setSimulationDateTime(SimulationTime.StartDateTime, datetime(2009, 10, 1, 12,30))
        >>>
        """
        dtme = create_string_buffer(newDateTime.strftime("%m/%d/%Y %H:%M:%S"))

        errcode = self.SWMMlibobj.swmm_setSimulationDateTime(c_int(timeType), dtme)
        self._error_check(errcode)
        

    def getSimUnit(self, unittype):
        """Get Simulation Units

        :param int unittype: Simulation Unit Type
        :return: Simulation Unit Type
        :rtype: str

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSimUnit(SimulationUnits.FlowUnits)
        >>> CFS
        >>> swmm_model.swmm_close()
        """
        value = c_int()
        errcode = self.SWMMlibobj.swmm_getSimulationUnit(unittype, byref(value))
        self._error_check(errcode)
        _flowunitnames = ["CFS","GPM","MGD","CMS","LPS","MLD"] # Temporary Solution (2017-1-2 BEM)
        return _flowunitnames[value.value]

    def getSimAnalysisSetting(self, settingtype):
        """Get Simulation Analysis Settings

        :param int settingtype: Analysis Option Setting
        :return: Simulation Analysis option setting
        :rtype: bool

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSimAnalysisSetting(SimAnalysisSettings.AllowPonding)
        >>> False
        >>> swmm_model.swmm_close()
        """
        value = c_int()
        errcode = self.SWMMlibobj.swmm_getSimulationAnalysisSetting(settingtype, byref(value))
        self._error_check(errcode)
        return bool(value.value)

    def getSimAnalysisSetting(self, paramtype):
        """Get Simulation Configuration Parameter

        :param int paramtype: Simulation Parameter Type
        :return: Simulation Analysis Parameter Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSimAnalysisSetting(SimulationParameters.RouteStep)
        >>> 300
        >>> swmm_model.swmm_close()
        """
        value = c_double()
        errcode = self.SWMMlibobj.swmm_getSimulationParam(paramtype, byref(value))
        self._error_check(errcode)
        return value.value
    
    def getProjectSize(self, objecttype):
        """Get Project Size: Number of Objects

        :param int objecttype: (member variable)
        :return: Object Count
        :rtype: int

        Examples:
        
        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getProjectSize(ObjectType.NODE)
        >>> 10
        >>> swmm_model.swmm_close()
        """
        count = c_int()
        errcode = self.SWMMlibobj.swmm_countObjects(objecttype, byref(count))
        self._error_check(errcode)
        return count.value
    
    def getObjectId(self, objecttype, index):
        """ Get Object ID name

        :param int objecttype: (member variable)
        :param index: ID Index
        :return: Object ID
        :rtype: string

        Examples:
        
        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getObjectId(ObjectType.NODE,35)
        >>> "example_id_name"
        >>>
        >>> swmm_model.swmm_close()
        """        
        ID = create_string_buffer(61)
        errcode = self.SWMMlibobj.swmm_getObjectId(objecttype,index, byref(ID))
        self._error_check(errcode)
        return ID.value

    def getObjectIDList(self, objecttype):
        """ Get Object ID list.

        :param int objecttype: (member variable)

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getObjectIDList(ObjectType.LINK)
        >>> ['C1:C2', 'C2', 'C3']
        >>>
        >>> swmm_model.swmm_close()
        >>>
        """
        IDS = []
        for index in range(self.getProjectSize(objecttype)):
            IDS.append(self.getObjectId(objecttype,index))

        return IDS

    def getObjectIDIndex(self, objecttype, ID):
        """
        Get Object ID Index. Mostly used as an internal function.
        
        """
        C_ID = c_char_p(ID)
        index = self.SWMMlibobj.project_findObject(objecttype, C_ID)
        if index != -1: return index
        else: raise Exception("ID Does Not Exist")

    def getNodeType(self, ID):
        """ Get Node Type (e.g. Junction, Outfall, Storage, Divider)

        :param str index: ID 
        :return: Object ID
        :rtype: int

        Examples:
        
        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getNodeType('J1')
        >>> 0
        >>>
        >>> swmm_model.getNodeType('J1') is NodeType.junction
        >>> True
        >>>
        >>> swmm_model.swmm_close()
        """

        index = self.getObjectIDIndex(ObjectType.NODE,ID)
        Ntype = c_int()
        errcode = self.SWMMlibobj.swmm_getNodeType(index, byref(Ntype))
        self._error_check(errcode)
        return Ntype.value

    def getLinkType(self, ID):
        """ Get Link Type (e.g. Conduit, Pump, Orifice, Weir, Outlet)

        :param str index: ID 
        :return: Object ID
        :rtype: int

        Examples:
        
        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLinkType('C1')
        >>> 3
        >>>
        >>> swmm_model.getLinkType('C1') is LinkType.weir
        >>> True
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.swmm_getObjectIDIndex(ObjectType.LINK,ID)
        Ltype = c_int()
        errcode = self.SWMMlibobj.swmm_getLinkType(index, byref(Ltype))
        self._error_check(errcode)
        return Ltype.value

    def getLinkConnections(self, ID):
        """ Get Link Connections (Upstream and Downstream Nodes).

        Interestingly, if the dynamic wave solver is used,
        when the input file is parsed and added to the SWMM5 data model,
        any negatively sloped conduits are reversed automatically. The
        swmm_getLinkConnections function always calls the _swmm_getLinkDirection
        function to ensure the user-assigned upstream ID and downstream IDs
        are in the correct order. This way, the function provides support for
        directed graphs automatically. 

        :param str index: ID 
        :return: (Upstream Node Index, Downstream Node Index)
        :rtype: tuple

        Examples:
        
        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLinkConnections('C1')
        >>> ('NodeUSID','NodeDSID')
        >>>
        >>> swmm_model.swmm_close()        
        """
        index = self.getObjectIDIndex(ObjectType.LINK,ID)
        
        USNodeIND = c_int()
        DSNodeIND = c_int()

        errcode = self.SWMMlibobj.swmm_getLinkConnections(index, byref(USNodeIND), byref(DSNodeIND))
        self._error_check(errcode)

        USNodeID = self.getObjectId(ObjectType.NODE, USNodeIND.value)
        DSNodeID = self.getObjectId(ObjectType.NODE, DSNodeIND.value)
        if self._getLinkDirection(ID) == 1:
            return (USNodeID, DSNodeID) # Return Tuple of Upstream and Downstream Node IDS
        elif self._getLinkDirection(ID) == -1: # link validations reverse the conduit direction if the slope is < 0
            return (DSNodeID, USNodeID) # Return Tuple of Upstream and Downstream Node IDS
            
    def _getLinkDirection(self, ID):
        """
        Internal Method: returns conduit flow direction

        :param str index: link ID
        :return: 1 for conduit flow from upstream node to downstream node
        and -1 for conduit flow from downstream node to upstream node
        :rtype: int
        """
        index = self.getObjectIDIndex(ObjectType.LINK,ID)
        
        direction = c_byte()
        errcode = self.SWMMlibobj.swmm_getLinkDirection(index, byref(direction))
        self._error_check(errcode)
        return direction.value

    def getNodeParam(self, ID, Parameter):
        """
        Get Node Parameter

        :param str ID: Node ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getNodeParam('J2',NodeParams.invertElev )
        >>> 13.392
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.getObjectIDIndex(ObjectType.NODE,ID)
        param = c_double()
        errcode = self.SWMMlibobj.swmm_getNodeParam(index,Parameter, byref(param))
        self._error_check(errcode)
        return param.value

    def setNodeParam(self, ID, Parameter, value):
        """
        Set Node Parameter

        :param str ID: Node ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getNodeParam('J2',NodeParams.invertElev, 19 )
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.getObjectIDIndex(ObjectType.NODE,ID)
        _val = c_double(value)
        errcode = self.SWMMlibobj.swmm_setNodeParam(index,Parameter, _val)
        self._error_check(errcode)

    def getLinkParam(self, ID, Parameter):
        """
        Get Link Parameter

        :param str ID: Link ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLinkParam('C1:C2',LinkParams.offset1 )
        >>> 0.0
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.getObjectIDIndex(ObjectType.LINK,ID)
        param = c_double()
        errcode = self.SWMMlibobj.swmm_getLinkParam(index,Parameter, byref(param))
        self._error_check(errcode)
        return param.value

    def setLinkParam(self, ID, Parameter, value):
        """
        Set Link Parameter

        :param str ID: Link ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLinkParam('C1:C2',LinkParams.offset1, 2 )
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.getObjectIDIndex(ObjectType.LINK,ID)
        _val = c_double(value)
        errcode = self.SWMMlibobj.swmm_setLinkParam(index,Parameter, _val)
        self._error_check(errcode)

    def getSubcatchParam(self, ID, Parameter):
        """
        Get Subcatchment Parameter

        :param str ID: Subcatchment ID
        :param int Parameter: Paramter (toolkitapi.SubcParams member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getLinkParam('S2',SubcParams.area )
        >>> 43561.596096880996
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.getObjectIDIndex(ObjectType.SUBCATCH,ID)
        param = c_double()
        errcode = self.SWMMlibobj.swmm_getSubcatchParam(index,Parameter, byref(param))
        self._error_check(errcode)
        return param.value

    def setSubcatchParam(self, ID, Parameter, value):
        """
        Set Subcatchment Parameter

        :param str ID: Subcatchment ID
        :param int Parameter: Paramter (toolkitapi.SubcParams member variable)

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.setLinkParam('S2',SubcParams.area, 100 )
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.getObjectIDIndex(ObjectType.SUBCATCH,ID)
        _val = c_double(value)
        errcode = self.SWMMlibobj.swmm_setSubcatchParam(index,Parameter, _val)
        self._error_check(errcode)

    def getSubcatchOutConnection(self, ID):
        """
        Get Subcatchment Outlet Connection.  This function return the type of loading
        surface and the ID. The two load to objects are nodes and other subcatchments.

        Nodes are ObjectType.NODE
        Subcatchments are ObjectType.SUBCATCH

        :param str ID: Subcatchment ID
        :param int Parameter: Paramter (toolkitapi.SubcParams member variable)
        :return: (Loading Surface Type, ID)
        :rtype: tuple

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.getSubcatchOutConnection('S2',SubcParams.area )
        >>> (2, 'J2')
        >>>
        >>> swmm_model.getSubcatchOutConnection('S2',SubcParams.area )[0] == ObjectType.NODE
        >>> True
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.getObjectIDIndex(ObjectType.SUBCATCH,ID)
        TYPELoadSurface = c_int()
        outindex = c_int()
        errcode = self.SWMMlibobj.swmm_getSubcatchOutConnection(index, byref(TYPELoadSurface), byref(outindex))
        self._error_check(errcode)

        if TYPELoadSurface.value == ObjectType.NODE:
            LoadID = self.getObjectId(ObjectType.NODE, outindex.value)
        if TYPELoadSurface.value == ObjectType.SUBCATCH:
            LoadID = self.getObjectId(ObjectType.SUBCATCH, outindex.value)
        return(TYPELoadSurface.value, LoadID)

    ############################################
    #### Active Simulation Result "Getters" ####
    ############################################

    def getCurrentSimualationTime(self):
        """
        Get Current Simulation DateTime in Python Format

        :return: Python Datetime
        :rtype: datetime
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        dtme = create_string_buffer(61)
        errcode = self.SWMMlibobj.swmm_getCurrentDateTimeStr(dtme)
        self._error_check(errcode)
        
        return datetime.strptime(dtme.value, "%b-%d-%Y %H:%M:%S")
    
    def getNodeResult(self, ID, resultType):
        """
        Get Node Result

        :param str ID: Node ID
        :param int Parameter: Paramter (toolkitapi.NodeResults member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        index = self.getObjectIDIndex(ObjectType.NODE,ID)
        result = c_double()
        
        errcode = self.SWMMlibobj.swmm_getNodeResult(index, resultType, byref(result))
        self._error_check(errcode)

        return result.value
    
    def getLinkResult(self, ID, resultType):
        """
        Get Link Result

        :param str ID: Link ID
        :param int Parameter: Paramter (toolkitapi.LinkResults member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        index = self.getObjectIDIndex(ObjectType.LINK,ID)
        result = c_double()
        
        errcode = self.SWMMlibobj.swmm_getLinkResult(index, resultType, byref(result))
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

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        index = self.getObjectIDIndex(ObjectType.SUBCATCH,ID)
        result = c_double()
        
        errcode = self.SWMMlibobj.swmm_getSubcatchResult(index, resultType, byref(result))
        self._error_check(errcode)

        return result.value
    
    ###############################################
    #### Active Simulation Parameter "Setters" ####
    ###############################################

    def setLinkSetting(self, ID, targetSetting):
        """
        Set Link Setting (Pumps, Orifices, Weirs)

        :param str ID: Link ID
        :param float targetSetting: New target setting which will be applied at the start of\
        the next routing step


        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        index = self.getObjectIDIndex(ObjectType.LINK,ID)
        targetSetting = c_double(targetSetting)
        errcode = self.SWMMlibobj.swmm_setLinkSetting(index, targetSetting)
        self._error_check(errcode)


    def setNodeInflow(self, ID, flowrate):
        """
        Set Node Inflow rate.  The flow rate should be in the user defined
        units.  The value is help constant in the model until it is redefined
        by the toolkit API. 

        :param str ID: Node ID
        :param float flowrate: New flow rate in the user-defined flow units

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
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
        
        index = self.getObjectIDIndex(ObjectType.NODE,ID)
        q = c_double(flowrate)
        errcode = self.SWMMlibobj.swmm_setNodeInflow(index, q)
        self._error_check(errcode)

class Nodes(object):
    """
    Node Iterator Methods

    :param object model: Open Model Instance 

    Examples:
        
    >>> swmm_model = pyswmm(r'\\.inp')
    >>> swmm_model.swmm_open()
    >>> for node in Nodes(swmmobject):
    ...     print node
    ...     print node.nodeid
    ...     print node.invertel
    ...     node.set_invertel(10)
    ...     print node.invertel
    ...
    >>> <swmm5.Node object at 0x031B0350>
    >>> J1
    >>> 20.728
    >>> 10.0
    >>> <swmm5.Node object at 0x030693D0>
    >>> J2
    >>> 13.392
    >>> 10.0
    >>> <swmm5.Node object at 0x031B0350>
    >>> J3
    >>> 6.547
    >>> 10.0
    >>> <swmm5.Node object at 0x030693D0>
    >>> J4
    >>> 0.0
    >>> 10.0
    >>> swmm_model.swmm_close()
    
    """
    def __init__(self, model):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model
        self.cuindex = 0
        self.nNodes = self._model.getProjectSize(ObjectType.NODE)
    def __iter__(self):
        return self
    
    def next(self):
        if self.cuindex < self.nNodes:
            nodeobject = Node(self._model, self.nodeid)
            self.cuindex+=1 #Next Iteration
            return nodeobject
        else:
            raise StopIteration()        
    def node(self, nodeid):
        "Node instance"
        return Node(self._model, nodeid)
    @property
    def nodeid(self):
        "Node ID"
        return self._model.getObjectId(ObjectType.NODE,self.cuindex)

class Node(object):
    """
    Node Methods
    
    :param object model: Open Model Instance 
    :param str nodeid: Node ID

    Examples:
        
    >>> swmm_model = pyswmm(r'\\.inp')
    >>> swmm_model.swmm_open()
    >>> node = Node(swmmobject, "J1")
    >>> print node.invertel
    >>> 10.0
    >>> swmm_model.swmm_close()
    
    """
    def __init__(self, model, nodeid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")        
        self._model = model
        self._nodeid = nodeid
    #Get Parameters
    @property
    def nodeid(self):
        """
        Get Node ID

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.nodeid
        >>> "J1"
        >>> swmm_model.swmm_close()
        """
        return self._nodeid      
    @property
    def ntype(self):
        """
        Get Node Type

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.ntype
        >>> 1
        >>> swmm_model.swmm_close()
        """
        return self._model.getNodeType(self._nodeid)
    @property
    def invertel(self):
        """
        Get Node Invert El

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.invertel
        >>> 10
        >>> swmm_model.swmm_close()
        """
        return self._model.getNodeParam(self._nodeid,NodeParams.invertElev)
    @property
    def fullDepth(self):
        """
        Get Node Full Depth

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.fullDepth
        >>> 10
        >>> swmm_model.swmm_close()
        """
        return self._model.getNodeParam(self._nodeid,NodeParams.fullDepth)
    @property
    def surDepth(self):
        """
        Get Node Surcharge Depth

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.surDepth
        >>> 100
        >>> swmm_model.swmm_close()
        """        
        return self._model.getNodeParam(self._nodeid,NodeParams.surDepth)
    @property
    def pondedArea(self):
        """
        Get Node Ponding Area

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.pondedArea
        >>> 100
        >>> swmm_model.swmm_close()
        """           
        return self._model.getNodeParam(self._nodeid,NodeParams.pondedArea)
    @property
    def initDepth(self):
        """
        Get Node Initial Depth at t0

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.initDepth
        >>> 100
        >>> swmm_model.swmm_close()
        """          
        return self._model.getNodeParam(self._nodeid,NodeParams.initDepth)
    ## Simulation Results
    @property
    def totalinflow(self):
        """
        Get Simulation Results for Total Inflow. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print node.totalinflow
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>> swmm_model.swmm_close()
        """             
        return self._model.getNodeResult(self._nodeid,NodeResults.totalinflow)  
    @property
    def outflow(self):
        """
        Get Simulation Results for Outflow. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print node.outflow
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>> swmm_model.swmm_close()
        """            
        return self._model.getNodeResult(self._nodeid,NodeResults.outflow)
    @property
    def losses(self):
        """
        Get Simulation Results for Outflow. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print node.losses
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>> swmm_model.swmm_close()
        """           
        return self._model.getNodeResult(self._nodeid,NodeResults.losses)
    @property
    def Volume(self):
        """
        Get Simulation Results for Current Volume. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print node.Volume
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>> swmm_model.swmm_close()
        """         
        return self._model.getNodeResult(self._nodeid,NodeResults.newVolume)
    @property
    def overflow(self):
        """
        Get Simulation Results for Overflow Volume (Flooding). If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print node.overflow
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>> swmm_model.swmm_close()
        """         
        return self._model.getNodeResult(self._nodeid,NodeResults.overflow)
    @property
    def Depth(self):
        """
        Get Simulation Results for Depth. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print node.Depth
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>> swmm_model.swmm_close()
        """  
        return self._model.getNodeResult(self._nodeid,NodeResults.newDepth)
    @property
    def Head(self):
        """
        Get Simulation Results for Head. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print node.Head
        ...     if (time <= 0.0): break
        ...
        >>> 10
        >>> 10.5
        >>> 10.9
        >>> 10.2
        >>> swmm_model.swmm_close()
        """  
        return self._model.getNodeResult(self._nodeid,NodeResults.newHead)
    @property
    def LatFlow(self):
        """
        Get Simulation Results for Lateral Inflow. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> while(True):
        ...     time = swmm_model.swmm_step()
        ...     print node.LatFlow
        ...     if (time <= 0.0): break
        ...
        >>> 1
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>> swmm_model.swmm_close()
        """  
        return self._model.getNodeResult(self._nodeid,NodeResults.newLatFlow)
    # Set Parameters
    def set_invertel(self, param):
        """
        Set Node parameter

        :param float param: New Parameter value
  
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.invertel
        >>> 10       
        >>> node.set_invertel(25)
        >>> print node.invertel
        >>> 25
        >>> swmm_model.swmm_close()
        """  
        self._model.setNodeParam(self._nodeid,NodeParams.invertElev, param)
    def set_fullDepth(self, param):
        """
        Set Node Depth

        :param float param: New Parameter value
  
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.fulldepth
        >>> 10       
        >>> node.set_fullDepth(25)
        >>> print node.fulldepth
        >>> 25
        >>> swmm_model.swmm_close()
        """ 
        self._model.setNodeParam(self._nodeid,NodeParams.fullDepth, param)
    def set_surDepth(self, param):
        """
        Set Node Surcharge Depth

        :param float param: New Parameter value
  
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.surDepth
        >>> 10       
        >>> node.set_surDepth(25)
        >>> print node.surDepth
        >>> 25
        >>> swmm_model.swmm_close()
        """ 
        self._model.setNodeParam(self._nodeid,NodeParams.surDepth, param)
    def set_pondedArea(self, param):
        """
        Set Node Ponding Area

        :param float param: New Parameter value
  
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.pondedArea
        >>> 0       
        >>> node.set_pondedArea(25)
        >>> print node.pondedArea
        >>> 25
        >>> swmm_model.swmm_close()
        """ 
        self._model.setNodeParam(self._nodeid,NodeParams.pondedArea, param)
    def set_initDepth(self, param):
        """
        Set Node Initial Depth

        :param float param: New Parameter value
  
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp')
        >>> swmm_model.swmm_open()
        >>> node = Node(swmmobject, "J1")
        >>> print node.initDepth
        >>> 0       
        >>> node.set_initDepth(25)
        >>> print node.initDepth
        >>> 25
        >>> swmm_model.swmm_close()
        """ 
        self._model.setNodeParam(self._nodeid,NodeParams.initDepth, param)














                                      
if __name__ == '__main__':
    test = pyswmm(inpfile = r"../test/TestModel1_weirSetting.inp",\
                   rptfile = r"../test/TestModel1_weirSetting.rpt",\
                   binfile = r"../test/TestModel1_weirSetting.out")
    test.swmm_open()

    print("Simulation Time Info")
    print("Start Time")
    print(test.getSimulationDateTime(SimulationTime.StartDateTime))
    print("End Time")
    print(test.getSimulationDateTime(SimulationTime.EndDateTime))
    print("Report Time")          
    print(test.getSimulationDateTime(SimulationTime.ReportStart))
    
    print("Simulation Units")
    print(test.getSimUnit(SimulationUnits.FlowUnits))

    print("Simulation Allow Ponding Option Selection")
    print(test.getSimAnalysisSetting(SimAnalysisSettings.AllowPonding))

    print("Simulation Routing Step")
    print(test.getSimAnalysisSetting(SimulationParameters.RouteStep))

    print("Number of Nodes")
    print(test.getProjectSize(ObjectType.NODE))
    
    print("Node ID")
    IDS = test.getObjectIDList(ObjectType.NODE)
    print(IDS)
    print('ID,Invert,Type')
    for ind, idd  in enumerate(IDS):
        print (ind,idd, test.getNodeParam( idd, NodeParams.invertElev ),\
              test.getNodeParam( idd, NodeParams.fullDepth ),\
              test.getNodeType( idd ))

    print("Link ID")
    print('ID,offset1,LinkConnections')
    IDS = test.getObjectIDList(ObjectType.LINK)
    print(IDS)
    for ind, idd  in enumerate(IDS):
        print(ind,idd, test.getLinkParam( idd, LinkParams.offset1 ), \
              test.getLinkConnections(idd))

    print("SUBCATCH ID")
    IDS = test.getObjectIDList(ObjectType.SUBCATCH)
    print(IDS)    
    for ind, idd  in enumerate(IDS):
        print(ind,idd, test.getSubcatchParam(idd, SubcParams.area),\
              test.getSubcatchOutConnection(idd))

    test.swmm_close()
