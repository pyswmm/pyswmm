from pyswmm import Simulation, Output
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH
from datetime import datetime


def test_simulation_output_with():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out')) as out:
        assert len(out.subcatchments) == 3
        assert len(out.nodes) == 5
        assert len(out.links) == 4
        assert len(out.pollutants) == 0

        # access with output methods
        flow_rate = out.link_series('C3', 'flow_rate')
        times = list(flow_rate.keys())
        assert times[0] == datetime(2015, 11, 1, 14, 1)
        assert times[-1] == datetime(2015, 11, 4)
        assert len(flow_rate) == 3480
        assert len(out.node_series('J1', 'flow_rate')) == 3480
        assert len(out.subcatch_series('S1', 'flow_rate')) == 3480
        assert len(out.system_series('evap_rate')) == 3480


def test_simulation_output():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    out = Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out'))
    out.open()
    assert len(out.subcatchments) == 3
    assert len(out.nodes) == 5
    assert len(out.links) == 4
    assert len(out.pollutants) == 0
    flow_rate = out.link_series('C3', 'flow_rate')
    times = list(flow_rate.keys())
    assert times[0] == datetime(2015, 11, 1, 14, 1)
    assert times[-1] == datetime(2015, 11, 4)
    assert len(flow_rate) == 3480
    out.close()
