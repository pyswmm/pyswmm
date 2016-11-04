'''
Python extensions for the SWMM5 Programmers toolkit

Open Water Analytics (http://wateranalytics.org/)

Developer: B. McDonnell

Last Update 5-12-14 

'''


import os
import sys
from toolkitapi import *

from ctypes import byref, c_double, c_float, c_int, c_char_p, create_string_buffer, c_byte

class SWMMException(Exception):
    pass

class pyswmm(object):
    '''
    Wrapper class to lead SWMM DLL object, then perform operations on
    the SWMM object that is created when the file is being loaded.
    '''
    SWMMlibobj = None
    ''' The variable that holds the ctypes Library object'''
    errcode = 0
    ''' Return code from the SWMM library functions'''
    Warnflag = False
    ''' A warning occured at some point during SWMM execution'''
    Errflag = False
    ''' A fatal error occured at some point during SWMM execution'''

    inpfile = ''
    rptfile = ''
    binfile = ''

    fileLoaded = False

    def __init__(self, inpfile = '', rptfile = '', binfile =''):
        '''
        Initialize the pyswmm object class

        Keyword arguments:
        * inpfile = the name of SWMM input file (default '')
        * rptfile = the report file to generate (default '')
        * binfile = the optional binary output file (default '')
        '''
        self.inpfile = inpfile
        self.rptfile = rptfile
        self.binfile = binfile

        def get_pkgpath():
            # Dynamically finds path to SWMM linking library
            import toolkitapi as tkp
            return os.path.dirname(tkp.__file__.replace('\\','/'))
        
        # The following should be un commented if using on mac
        #### darwin
        if 'darwin' in sys.platform:
            from ctypes import cdll
            libpath = os.getcwd()
            libswmm = '/pyswmm/data/Darwin/libswmm.dylib'
            self.SWMMlibobj = cdll.LoadLibrary(libpath+libswmm)

        #### windows
        if 'win32' in sys.platform:
            from ctypes import CDLL
            dllname = 'swmm5.dll'
            libswmm = get_pkgpath() + '\\data\\Windows\\' + dllname
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
        
        Arguments:
         * inpfile = SWMM input file
         * rptfile = output file to create
         * binfile = optional binary file to create
        
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
        
        Arguments:
         * inpfile = SWMM .inp input file (default to constructor value)
         * rptfile = Output file to create (default to constructor value)
         * binfile = Binary output file to create (default to constructor value)
        
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
        print self.errcode
        #self._error()
        #if self.errcode < 100:
            #self.fileLoaded = True
        
    def swmm_start(self):
        """frees all memory & files used by SWMM"""
        Save2Out = 1
        self.errcode = self.SWMMlibobj.swmm_start(c_int(Save2Out))
        
        self._error()
        if self.errcode < 100:
            self.fileLoaded = False
        
    def swmm_end(self):
        """frees all memory & files used by SWMM"""
        self.errcode = self.SWMMlibobj.swmm_end()
        
        self._error()
        if self.errcode < 100:
            self.fileLoaded = False
        
    def swmm_step(self):
        """ 

        """
        elapsed_time = c_double()
        self.SWMMlibobj.swmm_step(byref(elapsed_time))

        return elapsed_time.value

    def swmm_stride(self, advanceSeconds):
        """ 

        """
        if not hasattr(self, 'curSimTime'): self.curSimTime = 0.000001
        
        
        ctime = self.curSimTime
        #print ctime, advanceSeconds
        while advanceSeconds/3600./24. + ctime > self.curSimTime:
            elapsed_time = c_double()
            self.SWMMlibobj.swmm_step(byref(elapsed_time))
        
            #self.SWMMlibobj.swmm_stride(c_double(advanceSeconds), c_double(ctime), byref(elapsed_time))
            self.curSimTime = elapsed_time.value
            #print self.curSimTime
        return elapsed_time.value
        
    def swmm_report(self):
        """frees all memory & files used by SWMM"""
        self.errcode = self.SWMMlibobj.swmm_report()
        self.check_error()

    def check_error(self):
        self._error()
        if self.errcode < 100:
            self.fileLoaded = False   
            
    def swmm_close(self):
        """frees all memory & files used by SWMM"""
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
        
        Returns: int
         * version number of the DLL source code
        
        """
        return self.SWMMlibobj.swmm_getVersion()

    def swmm_getMassBalErr(self):
        runoffErr = c_float()
        flowErr = c_float()
        qualErr = c_float()

        self.errcode = self.SWMMlibobj.swmm_getMassBalErr(byref(runoffErr),\
                                                          byref(flowErr),\
                                                          byref(qualErr))
        self._error()
        
        return runoffErr.value, flowErr.value, qualErr.value

    #### NETWORK API FUNCTIONS
    def swmm_getProjectSize(self, objecttype):
        ''' Get Project Size: Number of Objects

        :param int objecttype: (member variable)
        
        :return: Object Count
        :rtype: int

        Examples:
        >>> swmm_model = pyswmm(r'//*.inp',r'//*.rpt',r'//*.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getProjectSize(ObjectType.NODE)
        >>> 10
        >>> swmm_model.swmm_close()
        '''
        count = c_int()
        self.errcode = self.SWMMlibobj.swmm_countObjects(objecttype, byref(count))
        if self.errcode != 0: raise Exception(self.errcode)
        return count.value
    
    def swmm_getObjectId(self, objecttype, index):
        ''' Get Object ID name

        :param int objecttype: (member variable)
        :param index: ID Index
        :return: Object ID
        :rtype: string

        Examples:
        >>> swmm_model = pyswmm(r'//*.inp',r'//*.rpt',r'//*.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getObjectId(ObjectType.NODE,35)
        >>> "example_id_name"
        >>>
        >>> swmm_model.swmm_close()
        '''        
        ID = create_string_buffer(61)
        self.errcode = self.SWMMlibobj.swmm_getObjectId(objecttype,index, byref(ID))
        if self.errcode != 0: raise Exception(self.errcode)
        return ID.value

    def swmm_getNodeType(self, index):
        ''' Get Node Type (e.g. Junction, Outfall, Storage, Divider)

        :param int index: ID Index
        :return: Object ID
        :rtype: int

        Examples:
        >>> swmm_model = pyswmm(r'//*.inp',r'//*.rpt',r'//*.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getNodeType(35)
        >>> 0
        >>>
        >>> swmm_model.swmm_getNodeType(35) is NodeType.junction
        >>> True
        >>>
        >>> swmm_model.swmm_close()
        '''          
        Ntype = c_int()
        self.errcode = self.SWMMlibobj.swmm_getNodeType(index, byref(Ntype))
        if self.errcode != 0: raise Exception(self.errcode)
        return Ntype.value

    def swmm_getLinkType(self, index):
        ''' Get Link Type (e.g. Conduit, Pump, Orifice, Weir, Outlet)

        :param int index: ID Index
        :return: Object ID
        :rtype: int

        Examples:
        >>> swmm_model = pyswmm(r'//*.inp',r'//*.rpt',r'//*.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getLinkType(35)
        >>> 3
        >>>
        >>> swmm_model.swmm_getLinkType(35) is LinkType.weir
        >>> True
        >>>
        >>> swmm_model.swmm_close()
        '''            
        Ltype = c_int()
        self.errcode = self.SWMMlibobj.swmm_getLinkType(index, byref(Ltype))
        if self.errcode != 0: raise Exception(self.errcode)
        return Ltype.value

    def swmm_getLinkConnections(self, index):
        ''' Get Link Connections (Upstream and Downstream Nodes).

        Interestingly, if the dynamic wave solver is used,
        when the input file is parsed and added to the SWMM5 data model,
        any negatively sloped conduits are reversed automatically. The
        swmm_getLinkConnections function always calls the _swmm_getLinkDirection
        function to ensure the user-assigned upstream ID and downstream IDs
        are in the correct order. This way, the functions provides support for
        directed graphs automatically. 

        :param int index: ID Index
        :return: (Upstream Node Index, Downstream Node Index)
        :rtype: tuple

        Examples:
        >>> swmm_model = pyswmm(r'//*.inp',r'//*.rpt',r'//*.out')
        >>> swmm_model.swmm_open()
        >>> swmm_model.swmm_getLinkConnections(35)
        >>> ('NodeUSID','NodeDSID')
        >>>
        >>> swmm_model.swmm_close()        
        '''
        USNodeIND = c_int()
        DSNodeIND = c_int()

        self.errcode = self.SWMMlibobj.swmm_getLinkConnections(index, byref(USNodeIND), byref(DSNodeIND))
        if self.errcode != 0: raise Exception(self.errcode)

        USNodeID = self.swmm_getObjectId(ObjectType.NODE, USNodeIND.value)
        DSNodeID = self.swmm_getObjectId(ObjectType.NODE, DSNodeIND.value)
        if self._swmm_getLinkDirection(index) == 1:
            return (USNodeID, DSNodeID) # Return Tuple of Upstream and Downstream Node IDS
        elif self._swmm_getLinkDirection(index) == -1: # link validations reverse the conduit direction if the slope is < 0
            return (DSNodeID, USNodeID) # Return Tuple of Upstream and Downstream Node IDS
            
    def _swmm_getLinkDirection(self, index):
        '''
        Internal Method: returns conduit flow direction

        :param int index: link ID index
        :return: 1 for conduit flow from upstream node to downstream node and -1 for conduit flow from downstream node to upstream node
        :rtype: int

        
        '''
        direction = c_byte()
        self.errcode = self.SWMMlibobj.swmm_getLinkDirection(index, byref(direction))
        if self.errcode !=0: raise Exception(self.errcode)
        return direction.value

    def swmm_getNodeParam(self, index, Parameter):
        param = c_double()
        self.errcode = self.SWMMlibobj.swmm_getNodeParam(index,Parameter, byref(param))
        if self.errcode != 0: raise Exception(self.errcode)
        return param.value

    def swmm_getLinkParam(self, index, Parameter):
        param = c_double()
        self.errcode = self.SWMMlibobj.swmm_getLinkParam(index,Parameter, byref(param))
        if self.errcode != 0: raise Exception(self.errcode)
        return param.value

    def swmm_getSubcatchParam(self, index, Parameter):
        param = c_double()
        self.errcode = self.SWMMlibobj.swmm_getSubcatchParam(index,Parameter, byref(param))
        if self.errcode != 0: raise Exception(self.errcode)
        return param.value

    def swmm_getSubcatchOutConnection(self, index):
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
    def swmm_getNodeResult(self, index, resultType):
        ''' Get Node Result at current time
        '''
        result = c_double()
        
        self.errcode = self.SWMMlibobj.swmm_getNodeResult(index, resultType, byref(result))
        if self.errcode != 0: raise Exception(self.errcode)

        return result.value
    
    def swmm_getLinkResult(self, index, resultType):
        ''' Get Link Result at current time
        '''
        result = c_double()
        
        self.errcode = self.SWMMlibobj.swmm_getLinkResult(index, resultType, byref(result))
        if self.errcode != 0: raise Exception(self.errcode)

        return result.value

    def swmm_getSubcatchResult(self, index, resultType):
        ''' Get Subcatchment Result at current time
        '''
        result = c_double()
        
        self.errcode = self.SWMMlibobj.swmm_getSubcatchResult(index, resultType, byref(result))
        if self.errcode != 0: raise Exception(self.errcode)

        return result.value
    
    ###############################################
    #### Active Simulation Parameter "Setters" ####
    ###############################################

    def swmm_setLinkSetting(self, index, targetSetting):
        ''' Set Link Setting
        '''
        targetSetting = c_double(targetSetting)
        self.errcode = self.SWMMlibobj.swmm_setLinkSetting(index, targetSetting)
        if self.errcode != 0: raise Exception(self.errcode)
        return 0


                                      
if __name__ == '__main__':
    test = pyswmm(inpfile = r"C:\PROJECTCODE\pyswmm\test\OutputTestModel522_SHORT.inp",\
                   rptfile = r"C:\PROJECTCODE\pyswmm\test\OutputTestModel522_SHORT.rpt",\
                   binfile = r"C:\PROJECTCODE\pyswmm\test\OutputTestModel522_SHORT.out")
    test.swmm_open()
    
    print test.swmm_getProjectSize(ObjectType.NODE)
    
    print "Node ID"
    IDS = {test.swmm_getObjectId(ObjectType.NODE,ind):ind for ind in range(test.swmm_getProjectSize(ObjectType.NODE))}
    print 'ID,Invert,Type'
    for idd in IDS.keys()[:10]:
        print IDS[idd],idd, test.swmm_getNodeParam( IDS[idd], NodeParams.invertElev ),\
              test.swmm_getNodeParam( IDS[idd], NodeParams.fullDepth ),\
              test.swmm_getNodeType( IDS[idd] )

    print "Link ID"
    print 'ID,offset1,LinkConnections'
    IDS = {test.swmm_getObjectId(ObjectType.LINK,ind):ind for ind in range(test.swmm_getProjectSize(ObjectType.LINK))}
    for idd in IDS.keys()[:10]:
        print IDS[idd],idd, test.swmm_getLinkParam( IDS[idd], LinkParams.offset1 ), \
              test.swmm_getLinkConnections(IDS[idd])

    print "SUBCATCH ID"
    IDS = {test.swmm_getObjectId(ObjectType.SUBCATCH,ind):ind for ind in range(test.swmm_getProjectSize(ObjectType.SUBCATCH))}
    for idd in IDS.keys()[:100]:
        print IDS[idd],idd, test.swmm_getSubcatchParam(IDS[idd], SubcParams.area),\
              test.swmm_getSubcatchOutConnection(IDS[idd])

    test.swmm_close()
