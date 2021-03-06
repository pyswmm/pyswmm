from pyswmm import Simulation, Output
from pyswmm.toolkitapi import subcatch_attribute, node_attribute, link_attribute, system_attribute
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

        assert len(out.subcatch_attribute('runoff_rate', 0)) == 3
        assert len(out.node_attribute('hydraulic_head', 0)) == 5
        assert len(out.link_attribute('flow_rate', 0)) == 4
        assert len(out.system_attribute('rainfall', 0)) == 1

        # no pollutant
        assert len(out.subcatch_result('S1', 0)) == len(subcatch_attribute) - 1
        assert len(out.node_result('J1', 0)) == len(node_attribute) - 1
        assert len(out.link_result('C1', 0)) == len(link_attribute) - 1
        assert len(out.system_result(0)) == len(system_attribute)


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
