'''
TestModel1_Current Time

Author: Bryant E. McDonnell (EmNet LLC)
Date: 11/12/2016


'''
import time
import os
import sys
from datetime import datetime, timedelta

#point to location of the pyswmm file
sys.path.append(os.getcwd()+'\\..\\pyswmm\\')

from swmm5 import PySWMM
from toolkitapi import *

swmmobject = PySWMM('./TestModel1_weirSetting.inp',\
                    './TestModel1_weirSetting.rpt',\
                    './TestModel1_weirSetting.out')
swmmobject.swmm_open()

print swmmobject.getNodeParam('J2',NodeParams.invertElev)#, 19 )
swmmobject.setNodeParam('J2',NodeParams.invertElev, 19 )
print swmmobject.getNodeParam('J2',NodeParams.invertElev)#, 19 )

print swmmobject.getLinkParam('C1:C2',LinkParams.offset1)#, 19 )
swmmobject.setLinkParam('C1:C2',LinkParams.offset1, 19 )
print swmmobject.getLinkParam('C1:C2',LinkParams.offset1)#, 19 )

print swmmobject.getSubcatchParam('S2',SubcParams.area)#, 19 )
swmmobject.setSubcatchParam('S2',SubcParams.area, 19 )
print swmmobject.getSubcatchParam('S2',SubcParams.area)#, 19 )

swmmobject.swmm_start()

i = 0
while(True):
    
    time = swmmobject.swmm_stride(600)
    i+=1     

    if (time <= 0.0):
        break
    if i %144==0: print i
    swmmobject.setLinkParam('C1:C2',LinkParams.qLimit, 0.25)
    
swmmobject.swmm_end()
#swmmobject.swmm_report()
swmmobject.swmm_close()

 
print("swmm_step() Check Passed")
