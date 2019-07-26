# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Local imports
from pyswmm import Node, Nodes, Simulation
from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import (MODEL_FULL_FEATURES_PATH,
                               MODEL_NODE_INFLOWS_PATH, MODEL_STORAGE_PUMP,
                               MODEL_STORAGE_PUMP_MGD, MODEL_WEIR_SETTING_PATH)
from pyswmm.utils.fixtures import get_model_files
import pyswmm.toolkitapi as tka
from pytest import approx
UT_PRECISION = 1  # %


def test_nodes_1():
    ''' pytest pyswmm/tests/test_nodes.py -k `test_nodes_1` '''
    swmmobject = PySWMM(MODEL_WEIR_SETTING_PATH)
    swmmobject.swmm_open()
    node = Node(swmmobject, "J1")
    assert(node.invert_elevation == 20.728)


def test_nodes_2():
    ''' pytest pyswmm/tests/test_nodes.py -k `test_nodes_2` '''
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        print("\n\n\nNODES\n")
        for node in Nodes(sim):
            assert ('J' in node.nodeid)
            node.invert_elevation = 10
            assert (node.invert_elevation == 10)


def test_nodes_3():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        print("\n\n\nNODES\n")
        j1 = Nodes(sim)["J1"]
        assert (j1.is_divider() == False)
        assert (j1.is_junction() == True)
        assert (j1.is_outfall() == False)
        assert (j1.is_storage() == False)


def test_nodes_4():
    swmmobject = PySWMM(*get_model_files(MODEL_WEIR_SETTING_PATH))
    swmmobject.swmm_open()

    print(swmmobject.getNodeParam('J2', tka.NodeParams.invertElev))
    swmmobject.setNodeParam('J2', tka.NodeParams.invertElev, 19)
    print(swmmobject.getNodeParam('J2', tka.NodeParams.invertElev))

    print(swmmobject.getLinkParam('C1:C2', tka.LinkParams.offset1))
    swmmobject.setLinkParam('C1:C2', tka.LinkParams.offset1, 19)
    print(swmmobject.getLinkParam('C1:C2', tka.LinkParams.offset1))

    print(swmmobject.getSubcatchParam('S2', tka.SubcParams.area))
    swmmobject.setSubcatchParam('S2', tka.SubcParams.area, 19)
    print(swmmobject.getSubcatchParam('S2', tka.SubcParams.area))

    swmmobject.swmm_start()
    i = 0
    while (True):
        time = swmmobject.swmm_stride(600)
        i += 1

        if (time <= 0.0):
            break

        if i % 144 == 0:
            print(i)

        swmmobject.setLinkParam('C1:C2', tka.LinkParams.qLimit, 0.25)

    swmmobject.swmm_end()
    swmmobject.swmm_close()
    print("swmm_step() Check Passed")


def test_nodes_5():
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    print("\n\n\nNODES\n")
    J5 = Nodes(sim)["J5"]

    for ind, step in enumerate(sim):
        if ind == 7:
            J5.generated_inflow(544.0)
        if ind > 8:
            assert (J5.lateral_inflow == approx(543.9, rel=UT_PRECISION))
            if ind % 1000 == 0:
                print(J5.lateral_inflow)
    sim.close()


def test_nodes_6():
    ''' pytest pyswmm/tests/test_nodes.py -k `test_nodes_6` '''
    sim = Simulation(MODEL_WEIR_SETTING_PATH)
    print("\n\n\nNODES\n")
    J5 = Nodes(sim)["J5"]

    for ind, step in enumerate(sim):
        pass

    assert(J5.statistics['peak_total_inflow']
           == approx(0.478, rel=UT_PRECISION))
    assert(J5.statistics['average_depth'] == approx(0.00017, rel=UT_PRECISION))
    assert(J5.statistics['surcharge_duration']
           == approx(0.0, rel=UT_PRECISION))
    assert(J5.statistics['max_ponded_volume'] == approx(0.0, rel=UT_PRECISION))
    assert(J5.statistics['courant_crit_duration']
           == approx(0.0, rel=UT_PRECISION))
    assert(J5.statistics['peak_lateral_inflowrate']
           == approx(0.0, rel=UT_PRECISION))
    assert(J5.statistics['flooding_duration'] == approx(0.0, rel=UT_PRECISION))
    assert(J5.statistics['peak_flooding_rate']
           == approx(0.0, rel=UT_PRECISION))
    assert(J5.statistics['lateral_infow_vol'] == approx(0.0, rel=UT_PRECISION))
    assert(J5.statistics['max_flooding_date']
           == approx(42309, rel=UT_PRECISION))
    assert(J5.statistics['max_depth_date'] == approx(42309, rel=UT_PRECISION))
    assert(J5.statistics['max_inflow_date'] == approx(42309, rel=UT_PRECISION))
    assert(J5.statistics['max_depth'] == approx(0.0292, rel=UT_PRECISION))
    assert(J5.statistics['flooding_volume'] == approx(0.0, rel=UT_PRECISION))
    assert(J5.statistics['max_report_depth']
           == approx(0.0286, rel=UT_PRECISION))
    sim.close()


def test_storage_7():
    ''' pytest pyswmm/tests/test_nodes.py -k `test_storage_7` '''
    sim = Simulation(MODEL_STORAGE_PUMP)
    print("\n\n\nSTORAGE\n")
    STOR1 = Nodes(sim)["SU1"]

    for ind, step in enumerate(sim):
        pass

    stats = STOR1.storage_statistics
    assert(stats['max_volume'] == approx(5000.0, rel=UT_PRECISION))
    assert(stats['peak_flowrate'] == approx(0.0, rel=UT_PRECISION))
    assert(stats['exfil_loss'] == approx(0.0, rel=UT_PRECISION))
    assert(stats['evap_loss'] == approx(0.0, rel=UT_PRECISION))
    assert(stats['average_volume'] == approx(4979.0, rel=UT_PRECISION))
    assert(stats['average_volume'] == approx(4980.0, rel=UT_PRECISION))
    assert(stats['max_vol_date'] == approx(42309.0, rel=UT_PRECISION))
    assert(stats['max_vol_date'] == approx(42310.0, rel=UT_PRECISION))
    assert(stats['initial_volume'] == approx(0.0, rel=UT_PRECISION))

    stats = STOR1.statistics
    assert(stats['peak_total_inflow'] == approx(2.9, rel=UT_PRECISION))
    assert(stats['peak_total_inflow'] == approx(3.1, rel=UT_PRECISION))

    assert(stats['average_depth'] == approx(4.9, rel=UT_PRECISION))
    assert(stats['average_depth'] == approx(5, rel=UT_PRECISION))

    assert(stats['flooding_duration'] == approx(57, rel=UT_PRECISION))
    assert(stats['flooding_duration'] == approx(58, rel=UT_PRECISION))

    assert(stats['peak_flooding_rate'] == approx(2.9, rel=UT_PRECISION))
    assert(stats['peak_flooding_rate'] == approx(3.1, rel=UT_PRECISION))

    assert(stats['lateral_infow_vol'] == approx(0.0, rel=UT_PRECISION))

    assert(stats['max_flooding_date'] == approx(42309, rel=UT_PRECISION))
    assert(stats['max_flooding_date'] == approx(42310, rel=UT_PRECISION))

    assert(stats['max_depth_date'] == approx(42309, rel=UT_PRECISION))
    assert(stats['max_depth_date'] == approx(42310, rel=UT_PRECISION))

    assert(stats['max_inflow_date'] == approx(42309, rel=UT_PRECISION))
    assert(stats['max_inflow_date'] == approx(42310, rel=UT_PRECISION))

    assert(stats['max_depth'] == approx(4.99, rel=UT_PRECISION))
    assert(stats['max_depth'] == approx(5.01, rel=UT_PRECISION))

    assert(stats['flooding_volume'] == approx(621390, rel=UT_PRECISION))
    assert(stats['flooding_volume'] == approx(621393, rel=UT_PRECISION))

    assert(stats['max_report_depth'] == approx(4.99, rel=UT_PRECISION))
    assert(stats['max_report_depth'] == approx(5.01, rel=UT_PRECISION))

    print(STOR1.statistics)
    sim.close()


def test_outfalls_8():
    ''' pytest pyswmm/tests/test_nodes.py -k `test_outfalls_8` '''
    sim = Simulation(MODEL_STORAGE_PUMP)
    print("\n\n\nOUTFALL\n")
    outfall = Nodes(sim)["J3"]

    for ind, step in enumerate(sim):
        pass
    stats = outfall.outfall_statistics
    outfall_cuinflow = outfall.cumulative_inflow
    sim.close()
    assert(stats['total_periods'] == approx(208796, rel=UT_PRECISION))
    assert(stats['pollutant_loading']['test']
           == approx(1756, rel=UT_PRECISION))
    assert(stats['pollutant_loading']['test']
           == approx(1756.2, rel=UT_PRECISION))
    assert(stats['average_flowrate'] == approx(8.9, rel=UT_PRECISION))
    assert(stats['average_flowrate'] == approx(9.0, rel=UT_PRECISION))
    assert(stats['peak_flowrate'] == approx(9.0, rel=UT_PRECISION))
    assert(stats['peak_flowrate'] == approx(9.1, rel=UT_PRECISION))
    assert(outfall_cuinflow == approx(1876800, rel=UT_PRECISION))
    assert(outfall_cuinflow == approx(1876900, rel=UT_PRECISION))


def test_outfalls_8_mgd():
    ''' pytest pyswmm/tests/test_nodes.py -k `test_outfalls_8_mgd` '''
    sim = Simulation(MODEL_STORAGE_PUMP_MGD)
    print("\n\n\nOUTFALL\n")
    outfall = Nodes(sim)["J3"]

    for ind, step in enumerate(sim):
        pass
    stats = outfall.outfall_statistics
    outfall_cuinflow = outfall.cumulative_inflow
    sim.close()

    assert(stats['total_periods'] == approx(208796, rel=UT_PRECISION))
    assert(stats['pollutant_loading']['test']
           == approx(1305.25, rel=UT_PRECISION))
    assert(stats['pollutant_loading']['test']
           == approx(1305.75, rel=UT_PRECISION))
    assert(stats['average_flowrate'] == approx(4.3, rel=UT_PRECISION))
    assert(stats['average_flowrate'] == approx(4.32, rel=UT_PRECISION))
    assert(stats['peak_flowrate'] == approx(4.33, rel=UT_PRECISION))
    assert(stats['peak_flowrate'] == approx(4.34, rel=UT_PRECISION))
    assert(outfall_cuinflow == approx(1395293, rel=UT_PRECISION))
    assert(outfall_cuinflow == approx(1395299, rel=UT_PRECISION) and
           outfall_cuinflow == approx(1395350, rel=UT_PRECISION))


def test_nodes_10():
    with Simulation(MODEL_NODE_INFLOWS_PATH) as sim:
        J1 = Nodes(sim)["J1"]
        outfall = Nodes(sim)["J3"]

        J1.generated_inflow(4)
        # Below Invert test
        outfall.outfall_stage(0)
        for ind, step in enumerate(sim):
            if ind == 1000:
                assert outfall.head >= outfall.invert_elevation
            if ind == 5000:
                outfall.outfall_stage(7)
            if ind == 5001:
                assert outfall.head == approx(7.00001, rel=UT_PRECISION)
                assert outfall.head == approx(6.99999, rel=UT_PRECISION)

            if ind == 50000:
                outfall.outfall_stage(13.5)

            if ind == 50001:
                assert outfall.head == approx(13.50001, rel=UT_PRECISION)
                assert outfall.head == approx(13.49999, rel=UT_PRECISION)
