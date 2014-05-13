#import sys
import os
    

import sys
sys.path.append('/Users/bryant/PROJECTCODE/OWA/pyswmm/trunk/pyswmm/data/')

from pyswmm import pyswmm

##from ctypes import cdll 
##libswmm = '/Users/bryant/PROJECTCODE/OWA/pyswmm/dll/libswmm.dylib'
##
##swmmobject = cdll.LoadLibrary(libswmm)
##swmmobject.swmm_run('/Users/bryant/PROJECTCODE/OWA/pyswmm/example/abridgedModel.inp',\
##                    '/Users/bryant/PROJECTCODE/OWA/pyswmm/example/abridgedModel.rpt',\
##                    '/Users/bryant/PROJECTCODE/OWA/pyswmm/example/abridgedModel.out')              
##swmmobject.swmm_start()
##swmmobject.swmm_end()
##swmmobject.swmm_report()
##swmmobject.swmm_close()

swmmobject = pyswmm('/Users/bryant/PROJECTCODE/OWA/pyswmm/example/parkinglot.inp',\
                    '/Users/bryant/PROJECTCODE/OWA/pyswmm/example/parkinglot.rpt',\
                    '/Users/bryant/PROJECTCODE/OWA/pyswmm/example/parkinglot.out')

swmmobject.swmmExec()
print swmmobject.swmm_getVersion()
print swmmobject.swmm_getMassBalErr()



##time = 0.0
##tend = 0.5
##swmmobject.swmm_open()
##swmmobject.swmm_start()
##
##while(True):
##    
##    time = swmmobject.swmm_step()
##    print time
##    if (time <= 0.0):
##        break
##    
##swmmobject.swmm_end()
##swmmobject.swmm_report()
##swmmobject.swmm_close()
    

