# Local imports
from pyswmm import Simulation
from pyswmm import LidControls, LidGroups, LidUnit
from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import MODEL_LIDS_PATH


def test_list_lid_controls():
    with Simulation(MODEL_LIDS_PATH) as sim:
        for i, control in enumerate(LidControls(sim)):
            if i == 0:
                assert(str(control) == 'LID')
            if i == 1:
                assert(str(control) == 'Green_LID')
           
def test_list_lid_groups():
    with Simulation(MODEL_LIDS_PATH) as sim:
        for i, group in enumerate(LidGroups(sim)):
            if i == 0:
                assert('subcatchment {} has {} lid units'.format(group,
                                                            len(group)) == 'subcatchment 1 has 0 lid units')
            if i == 1:
                assert('subcatchment {} has {} lid units'.format(group,
                                                            len(group)) == 'subcatchment 2 has 3 lid units')
            if i == 2:
                assert('subcatchment {} has {} lid units'.format(group,
                                                            len(group)) == 'subcatchment 3 has 0 lid units')
            if i == 3:
                assert('subcatchment {} has {} lid units'.format(group,
                                                            len(group)) == 'subcatchment 4 has 0 lid units')
            if i == 7:
                assert('subcatchment {} has {} lid units'.format(group,
                                                            len(group)) == 'subcatchment 8 has 0 lid units')

def test_list_lid_units():
    with Simulation(MODEL_LIDS_PATH) as sim:
        sub_2_lid_units = LidGroups(sim)["2"]
        for i, lid_unit in enumerate(sub_2_lid_units):
            if i == 0:
                assert(lid_unit.subcatchment == '2')
                assert(lid_unit.lid_control == 'LID')
            if i == 1:
                assert(lid_unit.subcatchment == '2')
                assert(lid_unit.lid_control == 'LID')
            if i == 2:
                assert(lid_unit.subcatchment == '2')
                assert(lid_unit.lid_control == 'Green_LID')

def test_lid_group_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        sub_2_lid_units = LidGroups(sim)["2"]
        sim.step_advance(900)
        for i, step in enumerate(sim):
            if i == 115:
                assert(sim.current_time.strftime('%Y-%m-%d %H:%M:%S') == '1998-01-02 05:00:00')
                assert(sub_2_lid_units.pervious_area == 50000)
                assert(round(sub_2_lid_units.flow_to_pervious, 4) == 0)
                assert(round(sub_2_lid_units.old_drain_flow, 4) >= 0.0008)
                assert(round(sub_2_lid_units.new_drain_flow, 4) >= 0.0008)

def test_lid_unit_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        sub_2_lid_units = LidGroups(sim)["2"]
        first_unit = sub_2_lid_units[0]
        assert(first_unit.unit_area == 10000)
        assert(first_unit.full_width == 20)
        assert(first_unit.initial_saturation == 0)
        assert(first_unit.from_impervious == 50)
        assert(first_unit.index == 0)
        assert(first_unit.number == 4)
        assert(first_unit.drain_subcatchment == -1)
        assert(first_unit.drain_node == 1)

        for i, step in enumerate(sim):
            if i == 2145:
                assert(first_unit.water_balance.inflow >= 8.9)
                assert(first_unit.water_balance.evaporation == 0)
                assert(first_unit.water_balance.infiltration >= 0.014)
                assert(first_unit.water_balance.surface_flow == 0)
                assert(first_unit.water_balance.drain_flow >= 3.35)
                assert(first_unit.water_balance.initial_volume == 3)
                assert(first_unit.water_balance.final_volume >= 8.5)
                assert(first_unit.surface.depth == 0)
                assert(first_unit.pavement.depth == 0)
                assert(first_unit.soil.moisture >= 0.2)
                assert(first_unit.storage.depth >= 6)
                assert(first_unit.dry_time == 21600)
                assert(first_unit.old_drain_flow >= 0.0005)
                assert(first_unit.new_drain_flow >= 0.0005)
                assert(first_unit.surface.flux_rate == 0)

def test_lid_control_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        LID = LidControls(sim)["LID"]
        Green_Lid = LidControls(sim)["Green_LID"]

        assert(LID.surface.thickness == 10)
        assert(LID.surface.void_fraction == 0.5)
        assert(LID.surface.roughness == 0.013)
        assert(LID.surface.slope == 1)
        assert(LID.surface.side_slope == 5)
        assert(round(LID.surface.alpha, 4) == 11.4615)
        assert(LID.can_overflow == False)
        assert(LID.soil.thickness == 30)
        assert(LID.soil.porosity == 0.5)
        assert(LID.soil.field_capacity == 0.2)
        assert(LID.soil.wilting_point == 0.1)
        assert(LID.soil.suction_head == 3.5)
        assert(LID.soil.k_saturated == 5.0)
        assert(LID.soil.k_slope == 10)
        assert(LID.storage.thickness == 40)
        assert(round(LID.storage.void_fraction, 4) == 0.75)
        assert(LID.storage.k_saturated == 0.5)
        assert(LID.storage.clog_factor == 0.2)
        assert(LID.pavement.thickness == 20)
        assert(round(LID.pavement.void_fraction, 4) == 0.15)
        assert(LID.pavement.impervious_fraction == 0.5)
        assert(LID.pavement.k_saturated == 100)
        assert(LID.pavement.clog_factor == 8)
        assert(LID.drain.coefficient == 0.5)
        assert(LID.drain.exponent == 0.5)
        assert(LID.drain.offset == 6)
        assert(LID.drain.delay == 6)
        # no drainmat
        assert(LID.drain_mat.thickness == 0)
        assert(LID.drain_mat.void_fraction == 0)
        assert(LID.drain_mat.roughness == 0)
        assert(LID.drain_mat.alpha == 0)

def test_lid_detailed_report():
    with Simulation(MODEL_LIDS_PATH) as sim:

        subLIDs = LidGroups(sim)

        sub_2_lids = subLIDs["2"]

        # first one defined in .inp
        first_LID_unit_on_sub_2 = sub_2_lids[0]
        # second one defined in .inp
        second_LID_unit_on_sub_2 = sub_2_lids[1]

        assert(first_LID_unit_on_sub_2.number == 4)
        assert(second_LID_unit_on_sub_2.number == 1)
        
        sim.step_advance(900)
        for i, step in enumerate(sim):
            if i == 20:
                assert(sim.current_time.strftime('%Y-%m-%d %H:%M:%S') == '1998-01-01 05:15:00')
                assert(first_LID_unit_on_sub_2.surface.inflow >= 0.47)
                assert(first_LID_unit_on_sub_2.evaporation == 0)
                assert(first_LID_unit_on_sub_2.surface.infiltration >= 0.47)
                assert(first_LID_unit_on_sub_2.pavement.percolation >= 0.47)
                assert(first_LID_unit_on_sub_2.soil.percolation >= 0.615)
                assert(first_LID_unit_on_sub_2.storage.exfiltration == 0)
                assert(first_LID_unit_on_sub_2.surface.outflow == 0)
                assert(first_LID_unit_on_sub_2.storage.drain == 0)
