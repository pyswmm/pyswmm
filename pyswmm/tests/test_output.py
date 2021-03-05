from pyswmm import Simulation, Output
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_simulation_output_with():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out')) as out:
        assert len(out.subcatchments) == 3
        assert len(out.nodes) == 4
        assert len(out.links) == 3
        assert len(out.pollutants) == 0

        # access with output methods
        # out.series()


def test_simulation_output():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    out = Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out'))
    out.open()
    assert len(out.subcatchments) == 3
    assert len(out.nodes) == 4
    assert len(out.links) == 3
    assert len(out.pollutants) == 0
    out.close()
