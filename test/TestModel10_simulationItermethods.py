'''
TestModel9_Current Time

Author: Bryant E. McDonnell (EmNet LLC)
Date: 11/12/2016


'''

#point to location of the pyswmm file
import sys
import os
sys.path.append(os.getcwd()+'\\..\\pyswmm\\')

from pyswmm import *
from links import Links
from nodes import Nodes

from random import randint


# TEST 2
with Simulation('TestModel1_weirSetting.inp') as sim:
    c1c2 = Links(sim)["C1:C2"]
    print c1c2.flow
    sim.step_advance(300)
    for ind, step in enumerate(sim):
        print c1c2.flow,c1c2.target_setting
        if c1c2.flow > 9.19:
            c1c2.target_setting = 0.9

    sim.report()



##    
##sim.report()
##sim.close()

#test 3
sim = Simulation('TestModel1_weirSetting.inp')
sim.execute()
