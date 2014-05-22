'''
Python extensions for the SWMM5 Programmers toolkit

Open Water Analytics (http://wateranalytics.org/)

Developer: B. McDonnell

Last Update 5-12-14 

'''


import os, sys
from ctypes import byref, cdll, windll, c_double, c_int, c_float
#from pkg_resources import resource_filename
#import platform

class SWMMException(Exception):
    pass

class pyswmm():
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
        
        '''
        as of 5-12-14 the shared library search feature is disabled. Reference pyepanet
        to see what the future will hold for this. resource_filename, I believe,
        is only a feature that works if this module is packaged for distribution - BEM
        '''
##        libnames = ['swmm']
##        for lib in libnames:
##            try:
##                if sys.platform in ['darwin']:
##                    #libswmm = resource_filename('pyswmm','data/Darwin/lin%s.dylib' % lib)

        # point to shared library, here
        libpath = 'C:\\Users\\mtryby\\Workspace\\GitRepo\\michaeltryby\\pyswmm'
        libswmm = '\\pyswmm\\data\\Windows\\swmm5_x86'
        self.SWMMlibobj = windll.LoadLibrary(libpath+libswmm)
##                
##            except Exception as E1:
##                if lib == libnames[-1]:
##                    raise E1
##                pass

    def isOpen(self):
        return self.fileLoaded
                
    def _error(self):
        """Print the error text the corresponds to the error code returned"""
        if not self.errcode: return
        errtxt = self.SWMMlibobj.swmmgeterror(self.errcode)
        sys.stdout.write(errtxt+"\n")
        if self.errcode >= 100:
            self.Errflag = True
            raise(SWMMException('Fatal error occured'))
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
        if inpfile is None: inpfile = self.inpfile
        if rptfile is None: rptfile = self.rptfile
        if binfile is None: binfile = self.binfile
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
        if rptfile is None: rptfile = self.rptfile
        if binfile is None: binfile = self.binfile
        self.SWMMlibobj.swmm_run(inpfile, rptfile, binfile)
        
    def swmm_open(self, inpfile=None, rptfile=None, binfile=None):
        """
        Opens SWMM input file & reads in network data
        
        Arguments:
         * inpfile = SWMM .inp input file (default to constructor value)
         * rptfile = Output file to create (default to constructor value)
         * binfile = Binary output file to create (default to constructor value)
        
        """
        if self.fileLoaded: self.swmm_close()
        if self.fileLoaded: 
            raise(SWMMException('Fatal error closing previously opened file'))
        if inpfile is None: inpfile = self.inpfile
        if rptfile is None: rptfile = self.rptfile
        if binfile is None: binfile = self.binfile
        self.errcode = self.SWMMlibobj.swmm_open(inpfile, rptfile, binfile)
        
        self._error()
        if self.errcode < 100:
            self.fileLoaded = True
        
    def swmm_start(self):
        """frees all memory & files used by SWMM"""
        self.errcode = self.SWMMlibobj.swmm_start()
        
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
        
        elapsed_time = c_double()
        self.SWMMlibobj.swmm_step(byref(elapsed_time))

        return elapsed_time.value

        
    def swmm_report(self):
        """frees all memory & files used by SWMM"""
        self.errcode = self.SWMMlibobj.swmm_report()
        
        self._error()
        if self.errcode < 100:
            self.fileLoaded = False   
            
    def swmm_close(self):
        """frees all memory & files used by SWMM"""
        self.errcode = self.SWMMlibobj.swmm_close()
        
        self._error()
        if self.errcode < 100:
            self.fileLoaded = False
    
    def swmmgeterror(self, iErrcode):
        """
        retrieves text of error/warning message
        
        Arguments:
         * errcode = error/warning code number
        
        Returns: string
         * text of error/warning message
        
        """
        sErrmsg = ctypes.create_string_buffer(256)
        self.errcode = self.SWMMlibobj.swmmgeterror(iErrcode, byref(sErrmsg), 256)
        self._error()
        return sErrmsg.value

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
