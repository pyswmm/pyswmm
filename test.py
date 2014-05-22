
import os
import sys

#point to location of the pyswmm file
sys.path.append(os.getcwd()+'\\pyswmm\\')

from swmm5 import pyswmm


# this checks the swmmExec process train...

swmmobject = pyswmm('./example/parkinglot.inp',\
                    './example/parkinglot.rpt',\
                    './example/parkinglot.out')

swmmobject.swmmExec()
print(swmmobject.swmm_getVersion())
print(swmmobject.swmm_getMassBalErr())


#this checks the swmm_step features

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
    

