# -*- coding: utf-8 -*-

from pyswmm import Simulation, Subcatchments

with Simulation('swmm_example.inp') as sim:
    S1 = Subcatchments(sim)["S1"]

    for step in sim:
        print(sim.current_time)
        print(S1.runoff)
