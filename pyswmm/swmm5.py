"""
Python extensions for the SWMM5 Programmers toolkit

Open Water Analytics (http://wateranalytics.org/)

Author: Bryant E. McDonnell (EmNet LLC)

Last Update: 11/10/2016 

"""


import os
import sys
from datetime import datetime
from ctypes import byref, c_double, c_float, c_int, c_char_p, create_string_buffer, c_byte, c_bool

from toolkitapi import *

__author__ = 'Bryant E. McDonnell (EmNet LLC) - bemcdonnell@gmail.com'
__copyright__ = 'Copyright (c) 2016 Bryant E. McDonnell'
__licence__ = 'BSD2'
__version__ = '0.2.1'

class SWMMException(Exception):
    pass

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
    >>> swmmobject.swmm_close()
    
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
    >>> swmmobject.swmm_start()
    >>> while(True):
    ...     time = swmmobject.swmm_step() # or swmm_stride()
    ...     if (time <= 0.0): break
    >>>
    >>> swmmobject.swmm_end()
    >>> swmmobject.swmm_report()
    >>> swmmobject.swmm_close()        
    """


    def __init__(self, inpfile = '', rptfile = '', binfile =''):
        """
        Initialize the pyswmm object class

        :param str inpfile: Name of SWMM input file (default '')
        :param str rptfile: Report file to generate (default '')
        :param str binfile: Optional binary output file (default '')
        """
        self.fileLoaded = False
        self.errcode = 0
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
            dllname = 'swmm5.dll'
            libswmm = get_pkgpath() + '\\swmmLinkedLibs\\Windows\\' + dllname
            self.SWMMlibobj = CDLL(libswmm)
            
    def _error(self):
        """Print the error text the corresponds to the error code returned"""
        if not self.errcode:
            return
        errtxt = self.SWMMlibobj.swmmgeterror(self.errcode)
        if self.errcode >= 100:
            self.Errflag = True
            raise(SWMMException('Fatal error occured {}'.format(errtxt)))
        else:
            self.Warnflag = True
        return
        
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
        >>> swmmobject.swmm_close()        
        """
        
        if inpfile is None:
            inpfile = self.inpfile
        if rptfile is None:
            if self.rptfile != '': rptfile = self.rptfile
            else: self.rptfile = self.inpfile.replace('.inp','.rpt')
        if binfile is None:
            if self.binfile != '': binfile = self.binfile
            else: self.binfile = self.inpfile.replace('.inp','.rpt') 
        sys.stdout.write("\n... SWMM Version 5.1")

        try:
            self.swmm_run()
            sys.stdout.write("\n... Run Complete")
        except:
            pass

        try:
            self.swmm_close()
            sys.stdout.write("\n... Closed")
        except:
            print('close fail')
            pass

        if self.Errflag: 
            sys.stdout.write("\n\n... SWMM completed. There are errors.\n")
        elif self.Warnflag:
            sys.stdout.write("\n\n... SWMM completed. There are warnings.\n")
        else:
            sys.stdout.write("\n\n... SWMM completed.\n")
            
    def swmm_run(self,inpfile=None, rptfile=None,binfile = None):
        if inpfile is None: inpfile = self.inpfile
        if rptfile is None:
            if self.rptfile != '': rptfile = self.rptfile
            else: self.rptfile = self.inpfile.replace('.inp','.rpt')
        if binfile is None:
            if self.binfile != '': binfile = self.binfile
            else: self.binfile = self.inpfile.replace('.inp','.rpt') 

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
        >>> swmmobject.swmm_close()          
        """
        if self.fileLoaded:
            self.swmm_close()
        if self.fileLoaded: 
            raise(SWMMException('Fatal error closing previously opened file'))
        if inpfile is None:
            inpfile = self.inpfile
        if rptfile is None:
            if self.rptfile != '': rptfile = self.rptfile
            else: self.rptfile = self.inpfile.replace('.inp','.rpt')
        if binfile is None:
            if self.binfile != '': binfile = self.binfile
            else: self.binfile = self.inpfile.replace('.inp','.rpt')            

        self.errcode = self.SWMMlibobj.swmm_open(c_char_p(inpfile),\
                                                 c_char_p(rptfile),\
                                                 c_char_p(binfile))
        #print self.errcode
        #self._error()
        #if self.errcode < 100:
            #self.fileLoaded = True
        
    def swmm_start(self, SaveOut2rpt = True):
        """Prepares to Start SWMM Simulation

        :param bool SaveOut2rpt: Save timeseries results to rpt file (default is False).

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmmobject.swmm_start()
        >>> while(True):
        ...     time = swmmobject.swmm_step()
        ...     if (time <= 0.0): break
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()
        
        """
        
        self.errcode = self.SWMMlibobj.swmm_start(c_bool(SaveOut2rpt))
        
        self._error()
        if self.errcode < 100:
            self.fileLoaded = False
        
    def swmm_end(self):
        """Ends SWMM Simulation

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmmobject.swmm_start()
        >>> while(True):
        ...     time = swmmobject.swmm_step()
        ...     if (time <= 0.0): break
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()
        """
        self.errcode = self.SWMMlibobj.swmm_end()
        
        self._error()
        if self.errcode < 100:
            self.fileLoaded = False
        
    def swmm_step(self):
        """ Advances SWMM Simulation by a single routing step

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmmobject.swmm_start()
        >>> while(True):
        ...     time = swmmobject.swmm_step()
        ...     if (time <= 0.0): break
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()
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
        ...     time = swmmobject.swmm_stride(600)
        ...     if (time <= 0.0): break
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()        
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
        >>> swmmobject.swmm_start()
        >>> while(True):
        ...     time = swmmobject.swmm_step()
        ...     if (time <= 0.0): break
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()
        """
        self.errcode = self.SWMMlibobj.swmm_report()
        self.check_error()

    def check_error(self):
        self._error()
        if self.errcode < 100:
            self.fileLoaded = False   
            
    def swmm_close(self):
        """ Closes model and supporting files and cleans up memory

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmmobject.swmm_start()
        >>> while(True):
        ...     time = swmmobject.swmm_step()
        ...     if (time <= 0.0): break
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()
        """
        self.errcode = self.SWMMlibobj.swmm_close()
        self.check_error()

##    def swmmgeterror(self, iErrcode):
##        """
##        retrieves text of error/warning message
##        
##        Arguments:
##         * errcode = error/warning code number
##        
##        Returns: string
##         * text of error/warning message
##        
##        """
##        sErrmsg = ctypes.create_string_buffer(256)
##        self.errcode = self.SWMMlibobj.swmmgeterror(iErrcode, byref(sErrmsg), 256)
##        self._error()
##        return sErrmsg.value

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

        self.errcode = self.SWMMlibobj.swmm_getMassBalErr(byref(runoffErr),\
                                                          byref(flowErr),\
                                                          byref(qualErr))
        self._error()
        
        return runoffErr.value, flowErr.value, qualErr.value

    #### NETWORK API FUNCTIONS
    def swmm_getSimulationDateTime(self, timeType):
        """
        Get Simulation Time Data (Based on SimulationTime options)

        :param int timeType: (toolkitapi.SimulationTime member variable)
        :return: datetime
        :rtype: datetime

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getSimulationDateTime(SimulationTime.StartDateTime)
        >>> 2015-11-01 14:00:00
        >>> swmm_model.swmm_getSimulationDateTime(SimulationTime.EndDateTime)
        >>> 2015-11-04 00:00:00
        >>> swmm_model.swmm_getSimulationDateTime(SimulationTime.ReportStart)
        >>> 2015-11-01 14:00:00     
        >>>
        >>> swmm_model.swmm_close()   
        """
        dtme = create_string_buffer(61)

        self.errcode = self.SWMMlibobj.swmm_getSimulationDateTime(c_int(timeType), dtme)
        if self.errcode != 0: raise Exception(self.errcode)
        
        return datetime.strptime(dtme.value, "%b-%d-%Y %H:%M:%S")

    def swmm_setSimulationDateTime(self, timeType, newDateTime):
        """
        Set Simulation Time Data (Based on SimulationTime options)

        :param int timeType: (toolkitapi.SimulationTime member variable)

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_setSimulationDateTime(SimulationTime.StartDateTime, datetime(2009, 10, 1, 12,30))
        >>>
        """
        dtme = create_string_buffer(newDateTime.strftime("%m/%d/%Y %H:%M:%S"))

        self.errcode = self.SWMMlibobj.swmm_setSimulationDateTime(c_int(timeType), dtme)
        if self.errcode != 0: raise Exception(self.errcode)
        

    def swmm_getSimUnit(self, unittype):
        """Get Simulation Units

        :param int unittype: Simulation Unit Type
        :return Simulation Unit Type
        :rtype: str

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getSimUnit(SimulationUnits.FlowUnits)
        >>> CFS
        >>> swmm_model.swmm_close()
        """
        value = c_int()
        self.errcode = self.SWMMlibobj.swmm_getSimulationUnit(unittype, byref(value))
        if self.errcode != 0: raise Exception(self.errcode)
        _flowunitnames = ["CFS","GPM","MGD","CMS","LPS","MLD"] # Temporary Solution (2017-1-2 BEM)
        return _flowunitnames[value.value]

    def swmm_getSimAnalysisSetting(self, settingtype):
        """Get Simulation Analysis Settings

        :param int settingtype: Analysis Option Setting
        :return Simulation Analysis option setting
        :rtype: bool

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getSimAnalysisSetting(SimAnalysisSettings.AllowPonding)
        >>> False
        >>> swmm_model.swmm_close()
        """
        value = c_int()
        self.errcode = self.SWMMlibobj.swmm_getSimulationAnalysisSetting(settingtype, byref(value))
        if self.errcode != 0: raise Exception(self.errcode)
        return bool(value.value)

    def swmm_getSimAnalysisSetting(self, paramtype):
        """Get Simulation Configuration Parameter

        :param int paramtype: Simulation Parameter Type
        :return Simulation Analysis Parameter Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getSimAnalysisSetting(SimulationParameters.RouteStep)
        >>> 300
        >>> swmm_model.swmm_close()
        """
        value = c_double()
        self.errcode = self.SWMMlibobj.swmm_getSimulationParam(paramtype, byref(value))
        if self.errcode != 0: raise Exception(self.errcode)
        return value.value
    
    def swmm_getProjectSize(self, objecttype):
        """Get Project Size: Number of Objects

        :param int objecttype: (member variable)
        
        :return: Object Count
        :rtype: int

        Examples:
        
        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getProjectSize(ObjectType.NODE)
        >>> 10
        >>> swmm_model.swmm_close()
        """
        count = c_int()
        self.errcode = self.SWMMlibobj.swmm_countObjects(objecttype, byref(count))
        if self.errcode != 0: raise Exception(self.errcode)
        return count.value
    
    def swmm_getObjectId(self, objecttype, index):
        """ Get Object ID name

        :param int objecttype: (member variable)
        :param index: ID Index
        :return: Object ID
        :rtype: string

        Examples:
        
        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getObjectId(ObjectType.NODE,35)
        >>> "example_id_name"
        >>>
        >>> swmm_model.swmm_close()
        """        
        ID = create_string_buffer(61)
        self.errcode = self.SWMMlibobj.swmm_getObjectId(objecttype,index, byref(ID))
        if self.errcode != 0: raise Exception(self.errcode)
        return ID.value

    def swmm_getObjectIDList(self, objecttype):
        """ Get Object ID list.

        :param int objecttype: (member variable)

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getObjectIDList(ObjectType.LINK)
        >>> ['C1:C2', 'C2', 'C3']
        >>>
        >>> swmm_model.swmm_close()
        >>>
        """
        IDS = []
        for index in range(self.swmm_getProjectSize(objecttype)):
            IDS.append(self.swmm_getObjectId(objecttype,index))

        return IDS

    def swmm_getObjectIDIndex(self, objecttype, ID):
        """
        Get Object ID Index. Mostly used as an internal function.
        
        """
        C_ID = c_char_p(ID)
        index = self.SWMMlibobj.project_findObject(objecttype, C_ID)
        if index != -1: return index
        else: raise Exception("ID Does Not Exist")

    def swmm_getNodeType(self, ID):
        """ Get Node Type (e.g. Junction, Outfall, Storage, Divider)

        :param str index: ID 
        :return: Object ID
        :rtype: int

        Examples:
        
        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getNodeType('J1')
        >>> 0
        >>>
        >>> swmm_model.swmm_getNodeType('J1') is NodeType.junction
        >>> True
        >>>
        >>> swmm_model.swmm_close()
        """

        index = self.swmm_getObjectIDIndex(ObjectType.NODE,ID)
        Ntype = c_int()
        self.errcode = self.SWMMlibobj.swmm_getNodeType(index, byref(Ntype))
        if self.errcode != 0: raise Exception(self.errcode)
        return Ntype.value

    def swmm_getLinkType(self, ID):
        """ Get Link Type (e.g. Conduit, Pump, Orifice, Weir, Outlet)

        :param str index: ID 
        :return: Object ID
        :rtype: int

        Examples:
        
        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getLinkType('C1')
        >>> 3
        >>>
        >>> swmm_model.swmm_getLinkType('C1') is LinkType.weir
        >>> True
        >>>
        >>> swmm_model.swmm_close()
        """
        index = self.swmm_getObjectIDIndex(ObjectType.LINK,ID)
        Ltype = c_int()
        self.errcode = self.SWMMlibobj.swmm_getLinkType(index, byref(Ltype))
        if self.errcode != 0: raise Exception(self.errcode)
        return Ltype.value

    def swmm_getLinkConnections(self, ID):
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
        >>> swmm_model.swmm_getLinkConnections('C1')
        >>> ('NodeUSID','NodeDSID')
        >>>
        >>> swmm_model.swmm_close()        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.LINK,ID)
        
        USNodeIND = c_int()
        DSNodeIND = c_int()

        self.errcode = self.SWMMlibobj.swmm_getLinkConnections(index, byref(USNodeIND), byref(DSNodeIND))
        if self.errcode != 0: raise Exception(self.errcode)

        USNodeID = self.swmm_getObjectId(ObjectType.NODE, USNodeIND.value)
        DSNodeID = self.swmm_getObjectId(ObjectType.NODE, DSNodeIND.value)
        if self._swmm_getLinkDirection(ID) == 1:
            return (USNodeID, DSNodeID) # Return Tuple of Upstream and Downstream Node IDS
        elif self._swmm_getLinkDirection(ID) == -1: # link validations reverse the conduit direction if the slope is < 0
            return (DSNodeID, USNodeID) # Return Tuple of Upstream and Downstream Node IDS
            
    def _swmm_getLinkDirection(self, ID):
        """
        Internal Method: returns conduit flow direction

        :param str index: link ID
        :return: 1 for conduit flow from upstream node to downstream node
        and -1 for conduit flow from downstream node to upstream node
        :rtype: int
        """
        index = self.swmm_getObjectIDIndex(ObjectType.LINK,ID)
        
        direction = c_byte()
        self.errcode = self.SWMMlibobj.swmm_getLinkDirection(index, byref(direction))
        if self.errcode !=0: raise Exception(self.errcode)
        return direction.value

    def swmm_getNodeParam(self, ID, Parameter):
        """
        Get Node Parameter

        :param str ID: Node ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getNodeParam('J2',NodeParams.invertElev )
        >>> 13.392
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.NODE,ID)
        param = c_double()
        self.errcode = self.SWMMlibobj.swmm_getNodeParam(index,Parameter, byref(param))
        if self.errcode != 0: raise Exception(self.errcode)
        return param.value

    def swmm_setNodeParam(self, ID, Parameter, value):
        """
        Set Node Parameter

        :param str ID: Node ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getNodeParam('J2',NodeParams.invertElev, 19 )
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.NODE,ID)
        _val = c_double(value)
        self.errcode = self.SWMMlibobj.swmm_setNodeParam(index,Parameter, _val)
        if self.errcode != 0: raise Exception(self.errcode)

    def swmm_getLinkParam(self, ID, Parameter):
        """
        Get Link Parameter

        :param str ID: Link ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getLinkParam('C1:C2',LinkParams.offset1 )
        >>> 0.0
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.LINK,ID)
        param = c_double()
        self.errcode = self.SWMMlibobj.swmm_getLinkParam(index,Parameter, byref(param))
        if self.errcode != 0: raise Exception(self.errcode)
        return param.value

    def swmm_setLinkParam(self, ID, Parameter, value):
        """
        Set Link Parameter

        :param str ID: Link ID
        :param int Parameter: Paramter (toolkitapi.NodeParams member variable)

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_setLinkParam('C1:C2',LinkParams.offset1, 2 )
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.LINK,ID)
        _val = c_double(value)
        self.errcode = self.SWMMlibobj.swmm_setLinkParam(index,Parameter, _val)
        if self.errcode != 0: raise Exception(self.errcode)

    def swmm_getSubcatchParam(self, ID, Parameter):
        """
        Get Subcatchment Parameter

        :param str ID: Subcatchment ID
        :param int Parameter: Paramter (toolkitapi.SubcParams member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getLinkParam('S2',SubcParams.area )
        >>> 43561.596096880996
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.SUBCATCH,ID)
        param = c_double()
        self.errcode = self.SWMMlibobj.swmm_getSubcatchParam(index,Parameter, byref(param))
        if self.errcode != 0: raise Exception(self.errcode)
        return param.value

    def swmm_setSubcatchParam(self, ID, Parameter, value):
        """
        Set Subcatchment Parameter

        :param str ID: Subcatchment ID
        :param int Parameter: Paramter (toolkitapi.SubcParams member variable)

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_setLinkParam('S2',SubcParams.area, 100 )
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.SUBCATCH,ID)
        _val = c_double(value)
        self.errcode = self.SWMMlibobj.swmm_setSubcatchParam(index,Parameter, _val)
        if self.errcode != 0: raise Exception(self.errcode)

    def swmm_getSubcatchOutConnection(self, ID):
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
        >>> swmm_model.swmm_getSubcatchOutConnection('S2',SubcParams.area )
        >>> (2, 'J2')
        >>>
        >>> swmm_model.swmm_getSubcatchOutConnection('S2',SubcParams.area )[0] == ObjectType.NODE
        >>> True
        >>>
        >>> swmm_model.swmm_close()    
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.SUBCATCH,ID)
        TYPELoadSurface = c_int()
        outindex = c_int()
        self.errcode = self.SWMMlibobj.swmm_getSubcatchOutConnection(index, byref(TYPELoadSurface), byref(outindex))
        if self.errcode != 0: raise Exception(self.errcode)

        if TYPELoadSurface.value == ObjectType.NODE:
            LoadID = self.swmm_getObjectId(ObjectType.NODE, outindex.value)
        if TYPELoadSurface.value == ObjectType.SUBCATCH:
            LoadID = self.swmm_getObjectId(ObjectType.SUBCATCH, outindex.value)
        return(TYPELoadSurface.value, LoadID)

    ############################################
    #### Active Simulation Result "Getters" ####
    ############################################

    def swmm_getCurrentSimualationTime(self):
        """
        Get Current Simulation DateTime in Python Format

        :return: Python Datetime
        :rtype: datetime
        
        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmmobject.swmm_start()
        >>> while(True):
        ...     time = swmmobject.swmm_step()
        ...     print swmmobject.swmm_getCurrentSimualationTime()
        ...     if (time <= 0.0): break
        ...
        >>> 2015-11-03 10:10:12
        >>> 2015-11-03 10:20:12
        >>> 2015-11-03 10:30:12
        >>> 2015-11-03 10:40:12
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()        
        """
        dtme = create_string_buffer(61)
        self.errcode = self.SWMMlibobj.swmm_getCurrentDateTimeStr(dtme)
        if self.errcode != 0: raise Exception(self.errcode)
        
        return datetime.strptime(dtme.value, "%b-%d-%Y %H:%M:%S")
    
    def swmm_getNodeResult(self, ID, resultType):
        """
        Get Node Result

        :param str ID: Node ID
        :param int Parameter: Paramter (toolkitapi.NodeResults member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmmobject.swmm_start()
        >>> while(True):
        ...     time = swmmobject.swmm_step()
        ...     print swmmobject.swmm_getNodeResult('J1', NodeResults.newDepth)
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()   
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.NODE,ID)
        result = c_double()
        
        self.errcode = self.SWMMlibobj.swmm_getNodeResult(index, resultType, byref(result))
        if self.errcode != 0: raise Exception(self.errcode)

        return result.value
    
    def swmm_getLinkResult(self, ID, resultType):
        """
        Get Link Result

        :param str ID: Link ID
        :param int Parameter: Paramter (toolkitapi.LinkResults member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmmobject.swmm_start()
        >>> while(True):
        ...     time = swmmobject.swmm_step()
        ...     print swmmobject.swmm_getLinkResult('J1', LinkResults.newFlow)
        ...     if (time <= 0.0): break
        ...
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()   
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.LINK,ID)
        result = c_double()
        
        self.errcode = self.SWMMlibobj.swmm_getLinkResult(index, resultType, byref(result))
        if self.errcode != 0: raise Exception(self.errcode)

        return result.value

    def swmm_getSubcatchResult(self, ID, resultType):
        """
        Get Subcatchment Result

        :param str ID: Subcatchment ID
        :param int Parameter: Paramter (toolkitapi.LinkResults member variable)
        :return: Paramater Value
        :rtype: float

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmmobject.swmm_start()
        >>> while(True):
        ...     time = swmmobject.swmm_step()
        ...     print swmmobject.swmm_getSubcatchResult('S3', SubcResults.newRunoff)
        ...     if (time <= 0.0): break
        ...
        >>> 0.01
        >>> 0.05
        >>> 0.09
        >>> 0.08
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()   
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.SUBCATCH,ID)
        result = c_double()
        
        self.errcode = self.SWMMlibobj.swmm_getSubcatchResult(index, resultType, byref(result))
        if self.errcode != 0: raise Exception(self.errcode)

        return result.value
    
    ###############################################
    #### Active Simulation Parameter "Setters" ####
    ###############################################

    def swmm_setLinkSetting(self, ID, targetSetting):
        """
        Set Link Setting (Pumps, Orifices, Weirs)

        :param str ID: Link ID
        :param float targetSetting: New target setting which will be applied at the start of\
        the next routing step


        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmmobject.swmm_start()
        >>> i = 0
        >>> while(True):
        ...     time = swmmobject.swmm_step()
        ...     i+=1
        ...
        ...     if i == 80:
        ...         swmmobject.swmm_setLinkSetting('C3',0.5)
        ...     if (time <= 0.0): break
        ...
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()   
        
        """
        index = self.swmm_getObjectIDIndex(ObjectType.LINK,ID)
        targetSetting = c_double(targetSetting)
        self.errcode = self.SWMMlibobj.swmm_setLinkSetting(index, targetSetting)
        if self.errcode != 0: raise Exception(self.errcode)


    def swmm_setNodeInflow(self, ID, flowrate):
        """
        Set Node Inflow rate.  The flow rate should be in the user defined
        units.  The value is help constant in the model until it is redefined
        by the toolkit API. 

        :param str ID: Node ID
        :param float flowrate: New flow rate in the user-defined flow units

        Examples:

        >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
        >>> swmm_model.swmm_open()
        >>> swmmobject.swmm_start()
        >>> i = 0
        >>> while(True):
        ...     if i == 80:
        ...         swmmobject.swmm_setNodeInflow('J1',4)
        ...     time = swmmobject.swmm_step()
        ...     i+=1
        ...
        >>>
        >>> swmmobject.swmm_end()
        >>> swmmobject.swmm_report()
        >>> swmmobject.swmm_close()           
        """
        
        index = self.swmm_getObjectIDIndex(ObjectType.NODE,ID)
        q = c_double(flowrate)
        self.errcode = self.SWMMlibobj.swmm_setNodeInflow(index, q)
        if self.errcode != 0: raise Exception(self.errcode)
                                      
if __name__ == '__main__':
    test = pyswmm(inpfile = r"../test/TestModel1_weirSetting.inp",\
                   rptfile = r"../test/TestModel1_weirSetting.rpt",\
                   binfile = r"../test/TestModel1_weirSetting.out")
    test.swmm_open()

    print("Simulation Time Info")
    print("Start Time")
    print(test.swmm_getSimulationDateTime(SimulationTime.StartDateTime))
    print("End Time")
    print(test.swmm_getSimulationDateTime(SimulationTime.EndDateTime))
    print("Report Time")          
    print(test.swmm_getSimulationDateTime(SimulationTime.ReportStart))
    
    print("Simulation Units")
    print(test.swmm_getSimUnit(SimulationUnits.FlowUnits))

    print("Simulation Allow Ponding Option Selection")
    print(test.swmm_getSimAnalysisSetting(SimAnalysisSettings.AllowPonding))

    print("Simulation Routing Step")
    print(test.swmm_getSimAnalysisSetting(SimulationParameters.RouteStep))

    print("Number of Nodes")
    print(test.swmm_getProjectSize(ObjectType.NODE))
    
    print("Node ID")
    IDS = test.swmm_getObjectIDList(ObjectType.NODE)
    print(IDS)
    print('ID,Invert,Type')
    for ind, idd  in enumerate(IDS):
        print (ind,idd, test.swmm_getNodeParam( idd, NodeParams.invertElev ),\
              test.swmm_getNodeParam( idd, NodeParams.fullDepth ),\
              test.swmm_getNodeType( idd ))

    print("Link ID")
    print('ID,offset1,LinkConnections')
    IDS = test.swmm_getObjectIDList(ObjectType.LINK)
    print(IDS)
    for ind, idd  in enumerate(IDS):
        print(ind,idd, test.swmm_getLinkParam( idd, LinkParams.offset1 ), \
              test.swmm_getLinkConnections(idd))

    print("SUBCATCH ID")
    IDS = test.swmm_getObjectIDList(ObjectType.SUBCATCH)
    print(IDS)    
    for ind, idd  in enumerate(IDS):
        print(ind,idd, test.swmm_getSubcatchParam(idd, SubcParams.area),\
              test.swmm_getSubcatchOutConnection(idd))

    test.swmm_close()
