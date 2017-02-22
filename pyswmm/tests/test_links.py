# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Local imports
from pyswmm import Link, Links, Simulation
from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_links_1():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        print("\n\n\nLINKS\n")
        c1c2 = Links(sim)["C1:C2"]
        print(c1c2.flow)
        print(c1c2.is_conduit())
        print(c1c2.is_pump())
        print(c1c2.is_orifice())
        print(c1c2.is_weir())
        print(c1c2.is_outlet())
        print(c1c2.connections)
        print(c1c2.inlet_node)
        print(c1c2.outlet_node)
        print(c1c2.average_head_loss)

        sim.step_advance(300)
        for ind, step in enumerate(sim):
            if c1c2.flow > 9.19:
                c1c2.target_setting = 0.9


def test_links_2():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for link in Links(sim):
            print(link)
            print(link.linkid)
            print(link.flow_limit)
            link.flow_limit = 10
            print(link.flow_limit)


#def test_links_3():
#    swmmobject = PySWMM(MODEL_WEIR_SETTING_PATH)
#    swmmobject.swmm_open()
#    swmmobject.swmmExec()
#    link = Link(swmmobject, "C2")
#    print(link.flow_limit)
#    swmmobject.swmm_close()
#    print("swmm_step() Check Passed")
