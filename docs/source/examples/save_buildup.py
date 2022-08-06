# -*- coding: utf-8 -*-

import csv
import os
from pyswmm import Simulation, Subcatchments

ts = 60 # routing step (sec)
sph = 3600 # seconds per hour
times = [(1/ts)*sph, (2/ts)*sph, (3/ts)*sph, (4/ts)*sph,
         (5/ts)*sph, (6/ts)*sph, (7/ts)*sph, (8/ts)*sph,
         (9/ts)*sph, (10/ts)*sph, (11/ts)*sph, (12/ts)*sph,]   # times to record buildup
i = 1
rec_step = 1

if not os.path.exists("buildup"):
    os.mkdir("buildup")

with Simulation('swmm_example.inp') as sim:

    for step in sim:

        if rec_step in times:
            with open('buildup/pollut_buildup'+str("%i" % i)+'.csv', 'w', newline='') as csvfile:
                load = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                load.writerow(['time:', sim.current_time])
                load.writerow(['Subcatchment', 'Loading'])
                for subcatchment in Subcatchments(sim):
                    load.writerow([subcatchment.subcatchmentid, subcatchment.buildup['test-pollutant']])
            i += 1

        rec_step += 1
