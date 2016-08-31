'''
Python extensions for the SWMM5 Programmers toolkit

Open Water Analytics (http://wateranalytics.org/)

Developer: B. McDonnell

Last Update 5-12-14 

'''


import os
import sys
from toolkitapi import *

from ctypes import byref, c_double, c_float, c_int, c_char_p, create_string_buffer

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
        
        # The following should be un commented if using on mac
        #### darwin
        if 'darwin' in sys.platform:
            from ctypes import cdll
            libpath = os.getcwd()
            libswmm = '/pyswmm/data/Darwin/libswmm.dylib'
            self.SWMMlibobj = cdll.LoadLibrary(libpath+libswmm)
        #### darwin



       #### windows
        if 'win32' in sys.platform:
            from ctypes import CDLL
            #from ctypes import windll
##            libpath = os.getcwd()
##            libswmm = '\\pyswmm\\data\\Windows\\swmm5_x86.dll'
##            libswmm = "C:\\PROJECTCODE\\pyswmm\\pyswmm\\swmm5.dll"
##            self.SWMMlibobj = CDLL(libswmm)
            libswmm = '.\\data\\Windows\\swmm5.dll'

##            self.SWMMlibobj = windll.LoadLibrary(libswmm)
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
            else self.rptfile = self.inpfile.replace('.inp','.rpt')
        if binfile is None:
            if self.binfile != '': binfile = self.binfile
            else self.binfile = self.inpfile.replace('.inp','.rpt') 
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
            else self.rptfile = self.inpfile.replace('.inp','.rpt')
        if binfile is None:
            if self.binfile != '': binfile = self.binfile
            else self.binfile = self.inpfile.replace('.inp','.rpt') 

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
            else self.rptfile = self.inpfile.replace('.inp','.rpt')
        if binfile is None:
            if self.binfile != '': binfile = self.binfile
            else self.binfile = self.inpfile.replace('.inp','.rpt')            

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
    def swmm_getProjectSize(self, ObjectType):
        count = c_int()
        self.errcode = self.SWMMlibobj.swmm_countObjects(ObjectType, byref(count))
        if self.errcode != 0: raise Exception(self.errcode)
        return count.value
    
    def swmm_getObjectId(self, ObjectType, index):
        ID = create_string_buffer(61)
        self.errcode = self.SWMMlibobj.swmm_getObjectId(ObjectType,index, byref(ID))
        if self.errcode != 0: raise Exception(self.errcode)
        return ID.value

    def swmm_getNodeParam(self, index, Parameter):
        param = c_float()
        self.errcode = self.SWMMlibobj.swmm_getNodeParam(index,Parameter, byref(param))
        if self.errcode != 0: raise Exception(self.errcode)
        return param.value
        
    
if __name__ == '__main__':
    test = pyswmm(inpfile = 'C:\\PROJECTCODE\\pyswmm\\pyswmm\\modelweirTravel.inp',\
                   rptfile = 'C:\\PROJECTCODE\\pyswmm\\pyswmm\\modelweirTravel.rpt',\
                   binfile = 'C:\\PROJECTCODE\\pyswmm\\pyswmm\\modelweirTravel.out')
    test.swmm_open()
    print test.swmm_getProjectSize(ObjectType.NODE)
    
    print "Node ID"
    IDS = {test.swmm_getObjectId(ObjectType.NODE,ind):ind for ind in range(test.swmm_getProjectSize(ObjectType.NODE))}
    print 'ID,Invert,Type'
    for idd in IDS.keys():
        print idd, test.swmm_getNodeParam( IDS[idd], NodeParams.invertElev ),\
              test.swmm_getNodeParam( IDS[idd], NodeParams.Type )

    print "Link ID"
    IDS = {test.swmm_getObjectId(ObjectType.LINK,ind):ind for ind in range(test.swmm_getProjectSize(ObjectType.LINK))}
    for idd in IDS.keys():
        print idd

    print "SUBCATCH ID"
    IDS = {test.swmm_getObjectId(ObjectType.SUBCATCH,ind):ind for ind in range(test.swmm_getProjectSize(ObjectType.SUBCATCH))}
    for idd in IDS.keys():
        print idd
