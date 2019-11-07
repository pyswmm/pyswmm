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
from pyswmm.tests.data import MODEL_FULL_FEATURES_PATH, MODEL_WEIR_SETTING_PATH, MODEL_SUBCATCH_STATS_PATH
from pytest import approx

UT_PRECISION = 1  # %


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


def test_subcatchments_3():
    with Simulation(MODEL_SUBCATCH_STATS_PATH) as sim:
        S1 = Subcatchments(sim)['S1']
        S2 = Subcatchments(sim)['S2']
        for ind, step in enumerate(sim):
            pass

        print(S1.statistics)
        print(S2.statistics)

        assert(S1.statistics['runon'] == approx(0.00, rel=UT_PRECISION)) # ft3
        assert(S1.statistics['peak_runoff_rate'] == approx(0.12, rel=UT_PRECISION)) # cfs
        assert(S1.statistics['evaporation'] == approx(0.00, rel=UT_PRECISION)) # ft3
        assert(S1.statistics['infiltration'] == approx(0.00, rel=UT_PRECISION)) # ft3
        assert(S1.statistics['precipitation'] == approx(0.12, rel=UT_PRECISION)) # in

        assert(S1.statistics['runoff'] == approx(1244.58, rel=UT_PRECISION)) # ft3
        assert(S2.statistics['evaporation'] == approx(0.00, rel=UT_PRECISION)) # ft3
        assert(S2.statistics['runoff'] == approx(0.00, rel=UT_PRECISION)) # ft3
        assert(S2.statistics['runon'] == approx(1207.74, rel=UT_PRECISION)) # ft3
        assert(S2.statistics['peak_runoff_rate'] == approx(0.00, rel=UT_PRECISION)) #cfs
        assert(S2.statistics['infiltration'] == approx(3476.57, rel=UT_PRECISION)) # ft3
        assert(S2.statistics['precipitation'] == approx(0.12, rel=UT_PRECISION)) # in


def test_nodes_3():
    with Simulation(MODEL_FULL_FEATURES_PATH) as sim:
        S2 = Subcatchments(sim)["S2"]  # Subcatchment

        for step in sim:
            print(S2.statistics)
