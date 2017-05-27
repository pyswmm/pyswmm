# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Local imports
from pyswmm import Simulation, Subcatchments
# from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_subcatchments_1():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        print("\n\n\nSubcatchments\n")
        S3 = Subcatchments(sim)["S3"]
        print(S3.area)
        print(S3.width)
        print(S3.connection)
        print(S3.percent_impervious)
        print(S3.slope)

        sim.step_advance(300)
        for ind, step in enumerate(sim):
            print(S3.runoff)


def test_subcatchments_2():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for subcatchment in Subcatchments(sim):
            print(subcatchment)
            print(subcatchment.subcatchmentid)
            print(subcatchment.curb_length)
            subcatchment.curb_length = 10
            print(subcatchment.curb_length)
