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

from swmm5 import pyswmm
from toolkitapi import *

swmmobject = pyswmm('./TestModel1_weirSetting.inp',\
                    './TestModel1_weirSetting.rpt',\
                    './TestModel1_weirSetting.out')
swmmobject.swmm_open()

print swmmobject.getSimulationDateTime(0)
print swmmobject.getSimulationDateTime(0) - timedelta(days = 10)
swmmobject.setSimulationDateTime(0, swmmobject.getSimulationDateTime(0) - timedelta(days = 10))
print swmmobject.getSimulationDateTime(0)

print swmmobject.getSimulationDateTime(1)
print swmmobject.getSimulationDateTime(1) - timedelta(days = 10)
swmmobject.setSimulationDateTime(1, swmmobject.getSimulationDateTime(1) - timedelta(days = 10))
print swmmobject.getSimulationDateTime(1)

print swmmobject.getSimulationDateTime(2)
print swmmobject.getSimulationDateTime(2) - timedelta(days = 10)
swmmobject.setSimulationDateTime(2, swmmobject.getSimulationDateTime(2) - timedelta(days = 10))
print swmmobject.getSimulationDateTime(2)


swmmobject.swmm_start()

i = 0
while(True):
    
    time = swmmobject.swmm_stride(600)
    i+=1
    print(swmmobject.getCurrentSimualationTime())
    print(type(swmmobject.getCurrentSimualationTime()))
     

    if (time <= 0.0):
        break
    if i %144==0: print i
    
swmmobject.swmm_end()
#swmmobject.swmm_report()
swmmobject.swmm_close()

 
print("swmm_step() Check Passed")
