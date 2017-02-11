'''
TestModel9_Current Time

Author: Bryant E. McDonnell (EmNet LLC)
Date: 11/12/2016


'''

#point to location of the pyswmm file
import sys
import os
sys.path.append(os.getcwd()+'\\..\\pyswmm\\')

from pyswmm import Simulation

from random import randint


# TEST 1
sim = Simulation('./TestModel1_weirSetting.inp')
for ind, step in enumerate(sim):
    print(step.getCurrentSimualationTime())
    sim.step_advance( randint(300,900) )
    
sim.report()
sim.close()

# TEST 2
with Simulation('./TestModel1_weirSetting.inp') as sim:
    for ind, step in enumerate(sim):
        sys.stdout.write("\rStatus: "+str(step.getCurrentSimualationTime()))
        sys.stdout.flush()
        
        sim.step_advance( randint(300,900) )

    sim.report()

# TEST 3
sim = Simulation('./TestModel1_weirSetting.inp')        
sim.execute()
