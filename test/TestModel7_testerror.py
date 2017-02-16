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



## Test rpt out 
swmmobject = PySWMM('./TestModel1_weirSetting.inp')
swmmobject.swmm_open()
swmmobject.swmmExec()

swmmobject.swmm_close()



## Test Warning
swmmobject = PySWMM('./TestModel1_weirSetting.inp',\
                    './TestModel1_weirSetting.rpt',\
                    './TestModel1_weirSetting.out')
swmmobject.swmm_open()

swmmobject.getLinkResult('C2',0)
swmmobject.swmm_close()

## Test PYSWMMException
swmmobject = PySWMM('./TestModel1_weirSetting.inp',\
                    './TestModel1_weirSetting.rpt',\
                    './TestModel1_weirSetting.out')
swmmobject.swmm_open()
print swmmobject.fileLoaded
swmmobject.swmm_open()
swmmobject.swmm_close()

## Test SWMMException
swmmobject = PySWMM('./TestModel11_weirSetting.inp')
swmmobject.swmm_open()
print swmmobject.fileLoaded
swmmobject.swmm_open()
swmmobject.swmm_close()


print("swmm_step() Check Passed")
