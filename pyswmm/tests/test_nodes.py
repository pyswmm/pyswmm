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
            assert (J5.lateral_inflow >= 543.9)
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
    
    assert(J5.statistics['peak_total_inflow'] >= 0.478)
    assert(J5.statistics['average_depth'] >= 0.00017)
    assert(J5.statistics['surcharge_duration'] >= 0.0)
    assert(J5.statistics['max_ponded_volume'] >= 0.0)
    assert(J5.statistics['courant_crit_duration'] >= 0.0)
    assert(J5.statistics['peak_lateral_inflowrate'] >= 0.0)
    assert(J5.statistics['flooding_duration'] >= 0.0)
    assert(J5.statistics['peak_flooding_rate'] >= 0.0)
    assert(J5.statistics['lateral_infow_vol'] >= 0.0)
    assert(J5.statistics['max_flooding_date'] >= 42309)
    assert(J5.statistics['max_depth_date'] >= 42309)
    assert(J5.statistics['max_inflow_date'] >= 42309)
    assert(J5.statistics['max_depth'] >= 0.0292)
    assert(J5.statistics['flooding_volume'] >= 0.0)
    assert(J5.statistics['max_report_depth'] >= 0.0286)
    sim.close()


def test_storage_7():
    ''' pytest pyswmm/tests/test_nodes.py -k `test_storage_7` '''
    sim = Simulation(MODEL_STORAGE_PUMP)
    print("\n\n\nSTORAGE\n")
    STOR1 = Nodes(sim)["SU1"]

    for ind, step in enumerate(sim):
        pass

    stats = STOR1.storage_statistics
    assert(stats['max_volume'] ==  5000.0)
    assert(stats['peak_flowrate'] ==  0.0)
    assert(stats['exfil_loss'] ==  0.0)
    assert(stats['evap_loss'] ==  0.0)
    assert(stats['average_volume'] >=  4979.0)
    assert(stats['average_volume'] <=  4980.0)
    assert(stats['max_vol_date'] >=  42309.0)
    assert(stats['max_vol_date'] <=  42310.0)
    assert(stats['initial_volume'] ==  0.0)

    stats = STOR1.statistics
    assert(stats['peak_total_inflow'] >= 2.9)
    assert(stats['peak_total_inflow'] <= 3.1)
    
    assert(stats['average_depth'] >= 4.9)
    assert(stats['average_depth'] <= 5)

    assert(stats['flooding_duration'] >= 57)
    assert(stats['flooding_duration'] <= 58)
    
    assert(stats['peak_flooding_rate'] >= 2.9)
    assert(stats['peak_flooding_rate'] <= 3.1)
    
    assert(stats['lateral_infow_vol'] == 0.0)
    
    assert(stats['max_flooding_date'] >= 42309)
    assert(stats['max_flooding_date'] <= 42310)
    
    assert(stats['max_depth_date'] >= 42309)
    assert(stats['max_depth_date'] <= 42310)
    
    assert(stats['max_inflow_date'] >= 42309)
    assert(stats['max_inflow_date'] <= 42310)

    assert(stats['max_depth'] >= 4.99)
    assert(stats['max_depth'] <= 5.01)
    
    assert(stats['flooding_volume'] >= 621390)
    assert(stats['flooding_volume'] <= 621393)
    
    assert(stats['max_report_depth'] >= 4.99)
    assert(stats['max_report_depth'] <= 5.01)

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
    assert(stats['total_periods'] ==  208796)
    assert(stats['pollutant_loading']['test'] >= 1756)
    assert(stats['pollutant_loading']['test'] <= 1756.2)
    assert(stats['average_flowrate'] >= 8.9)
    assert(stats['average_flowrate'] <= 9.0)
    assert(stats['peak_flowrate'] > 9.0)
    assert(stats['peak_flowrate'] < 9.1)
    assert(outfall_cuinflow >= 1876800)
    assert(outfall_cuinflow <= 1876900)
    

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
    
    assert(stats['total_periods'] ==  208796)
    assert(stats['pollutant_loading']['test'] >= 1305.25)
    assert(stats['pollutant_loading']['test'] <= 1305.75)
    assert(stats['average_flowrate'] >= 4.3)
    assert(stats['average_flowrate'] <= 4.32)
    assert(stats['peak_flowrate'] > 4.33)
    assert(stats['peak_flowrate'] < 4.34)
    assert(outfall_cuinflow >= 1395293)
    assert(outfall_cuinflow >= 1395299 and
           outfall_cuinflow <= 1395350)



def test_nodes_10():
    with Simulation(MODEL_NODE_INFLOWS_PATH) as sim:
        J1 = Nodes(sim)["J1"]
        outfall = Nodes(sim)["J3"]

        J1.generated_inflow(4)
        #Below Invert test
        outfall.outfall_stage(0)
        for ind, step in enumerate(sim):
            if ind == 1000:
                assert outfall.head >= outfall.invert_elevation
            if ind == 5000:
                outfall.outfall_stage(7)
            if ind == 5001:
                assert outfall.head <= 7.00001
                assert outfall.head >= 6.99999

            if ind == 50000:
                outfall.outfall_stage(13.5)

            if ind == 50001:
                assert outfall.head <= 13.50001
                assert outfall.head >= 13.49999
