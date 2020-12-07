from pyswmm import Simulation, RainGages, SystemStats
from pyswmm.tests.data import MODEL_RAIN
from pyswmm.toolkitapi import RainGageResults


def test_api_rainfall():
    with Simulation(MODEL_RAIN) as sim:
        check = 0

        sim._model.setGagePrecip("Gage1", 10.00)
        for ind, step in enumerate(sim):
            sim._model.setGagePrecip("Gage1", 10.00)
            x = sim._model.getGagePrecip("Gage1", RainGageResults.total_precip)

            if round(x, 2) == 10.0:
                check += 1
    assert(check == 718)


def test_rainfall():
    with Simulation(MODEL_RAIN) as sim:
        rg = RainGages(sim)["Gage1"]
        assert(rg.raingageid == "Gage1")

        sim.step_advance(3600)
        for ind, step in enumerate(sim):
            if ind > 0 and ind < 5:
                assert(rg.total_precip == 1)
                assert(rg.rainfall == 1)
                assert(rg.snowfall == 0)

            if ind == 5:
                rg.total_precip = 10

            if ind >= 6:
                assert(int(rg.total_precip) == 10)
                assert(int(rg.rainfall) == 10)
                assert(int(rg.snowfall) == 0)

        stats = SystemStats(sim)
        assert(int(stats.runoff_stats.rainfall) == 65)
