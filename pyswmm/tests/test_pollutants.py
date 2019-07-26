# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2017 Katherine M. Ratliff
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Local imports
from pyswmm import Simulation, Subcatchments
# from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import MODEL_POLLUTANTS_PATH


def test_pollutants_1():
    with Simulation(MODEL_POLLUTANTS_PATH) as sim:
        S1 = Subcatchments(sim)["S1"]
        S2 = Subcatchments(sim)["S2"]
        S3 = Subcatchments(sim)["S3"]

        for step in sim:
            print(S1.buildup)
            print(S2.buildup)
            print(S3.buildup)

            print(S1.concPonded)
            print(S2.concPonded)
            print(S3.concPonded)

        assert S1.buildup['test-pollutant'] == 25.000
        assert S2.buildup['test-pollutant'] == 25.000
        assert S3.buildup['test-pollutant'] == 25.000

        assert 9.99999 <= S1.concPonded['test-pollutant'] <= 10.00001
        assert 9.99999 <= S2.concPonded['test-pollutant'] <= 10.00001
        assert 9.99999 <= S3.concPonded['test-pollutant'] <= 10.00001

