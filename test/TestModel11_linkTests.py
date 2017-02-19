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

# TEST 2
with Simulation('TestModel1_weirSetting.inp') as sim:
    c1c2 = Links(sim)["C1:C2"]
    print c1c2.flow

    print c1c2.is_conduit()
    print c1c2.is_pump()
    print c1c2.is_orifice()
    print c1c2.is_weir()
    print c1c2.is_outlet()

    print c1c2.link_connections
    print c1c2.inlet_node
    print c1c2.outlet_node

    print c1c2.average_head_loss
    
##    sim.step_advance(300)
##    for ind, step in enumerate(sim):
##        print c1c2.flow,c1c2.target_setting
##        if c1c2.flow > 9.19:
##            c1c2.target_setting = 0.9
    

