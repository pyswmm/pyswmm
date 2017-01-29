'''
TestModel1_Current Time

Author: Bryant E. McDonnell (EmNet LLC)
Date: 11/12/2016


'''
import time
import os
import sys

#point to location of the pyswmm file
sys.path.append(os.getcwd()+'\\..\\pyswmm\\')

from swmm5 import pyswmm
from toolkitapi import *

swmmobject = pyswmm('./TestModel1_weirSetting.inp',\
                    './TestModel1_weirSetting.rpt',\
                    './TestModel1_weirSetting.out')
swmmobject.swmm_open()
print swmmobject.getSimulationDateTime(0)
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
swmmobject.swmm_report()
swmmobject.swmm_close()

 
print("swmm_step() Check Passed")
