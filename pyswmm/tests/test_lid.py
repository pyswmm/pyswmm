# Local imports
from pyswmm import Simulation
from pyswmm import LidControls, LidGroups
from pyswmm.tests.data import MODEL_LIDS_PATH
from pytest import approx
UT_PRECISION = 1  # %


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
                assert(sim.current_time.strftime(
                    '%Y-%m-%d %H:%M:%S') == '1998-01-02 05:00:00')
                assert(
                    sub_2_lid_units.pervious_area == approx(
                        50000, rel=UT_PRECISION))
                assert(
                    sub_2_lid_units.flow_to_pervious == approx(
                        0, rel=UT_PRECISION))
                assert(
                    sub_2_lid_units.old_drain_flow == approx(
                        0.0008, rel=UT_PRECISION))
                assert(
                    sub_2_lid_units.new_drain_flow == approx(
                        0.0008, rel=UT_PRECISION))


def test_lid_unit_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        sub_2_lid_units = LidGroups(sim)["2"]
        first_unit = sub_2_lid_units[0]
        assert(first_unit.unit_area == approx(10000, rel=UT_PRECISION))
        assert(first_unit.full_width == approx(20, rel=UT_PRECISION))
        assert(first_unit.initial_saturation == approx(0, rel=UT_PRECISION))
        assert(first_unit.from_impervious == approx(50, rel=UT_PRECISION))
        assert(first_unit.index == 0)
        assert(first_unit.number == 4)
        assert(first_unit.drain_subcatchment == -1)
        assert(first_unit.drain_node == 1)

        for i, step in enumerate(sim):
            if i == 2145:
                assert(
                    first_unit.water_balance.inflow == approx(
                        8.9, rel=UT_PRECISION))
                assert(
                    first_unit.water_balance.evaporation == approx(
                        0, rel=UT_PRECISION))
                assert(
                    first_unit.water_balance.infiltration == approx(
                        0.014, rel=UT_PRECISION))
                assert(
                    first_unit.water_balance.surface_flow == approx(
                        0, rel=UT_PRECISION))
                assert(
                    first_unit.water_balance.drain_flow == approx(
                        3.35, rel=UT_PRECISION))
                assert(
                    first_unit.water_balance.initial_volume == approx(
                        3, rel=UT_PRECISION))
                assert(
                    first_unit.water_balance.final_volume == approx(
                        8.5, rel=UT_PRECISION))
                assert(first_unit.surface.depth == approx(0, rel=UT_PRECISION))
                assert(
                    first_unit.pavement.depth == approx(
                        0, rel=UT_PRECISION))
                assert(
                    first_unit.soil.moisture == approx(
                        0.2, rel=UT_PRECISION))
                assert(first_unit.storage.depth == approx(6, rel=UT_PRECISION))
                assert(first_unit.dry_time == approx(21600, rel=UT_PRECISION))
                assert(
                    first_unit.old_drain_flow == approx(
                        0.0005, rel=UT_PRECISION))
                assert(
                    first_unit.new_drain_flow == approx(
                        0.0005, rel=UT_PRECISION))
                assert(
                    first_unit.surface.flux_rate == approx(
                        0, rel=UT_PRECISION))


def test_lid_control_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        LID = LidControls(sim)["LID"]
        Green_Lid = LidControls(sim)["Green_LID"]

        assert(LID.surface.thickness == approx(10, rel=UT_PRECISION))
        assert(LID.surface.void_fraction == approx(0.5, rel=UT_PRECISION))
        assert(LID.surface.roughness == approx(0.013, rel=UT_PRECISION))
        assert(LID.surface.slope == approx(1, rel=UT_PRECISION))
        assert(LID.surface.side_slope == approx(5, rel=UT_PRECISION))
        assert(LID.surface.alpha == approx(11.4615, rel=UT_PRECISION))
        assert(LID.can_overflow == False)
        assert(LID.soil.thickness == approx(30, rel=UT_PRECISION))
        assert(LID.soil.porosity == approx(0.5, rel=UT_PRECISION))
        assert(LID.soil.field_capacity == approx(0.2, rel=UT_PRECISION))
        assert(LID.soil.wilting_point == approx(0.1, rel=UT_PRECISION))
        assert(LID.soil.suction_head == approx(3.5, rel=UT_PRECISION))
        assert(LID.soil.k_saturated == approx(5.0, rel=UT_PRECISION))
        assert(LID.soil.k_slope == approx(10, rel=UT_PRECISION))
        assert(LID.storage.thickness == approx(40, rel=UT_PRECISION))
        assert(LID.storage.void_fraction == approx(0.75, rel=UT_PRECISION))
        assert(LID.storage.k_saturated == approx(0.5, rel=UT_PRECISION))
        assert(LID.storage.clog_factor == approx(0.2, rel=UT_PRECISION))
        assert(LID.pavement.thickness == approx(20, rel=UT_PRECISION))
        assert(LID.pavement.void_fraction == approx(0.15, rel=UT_PRECISION))
        assert(LID.pavement.impervious_fraction ==
               approx(0.5, rel=UT_PRECISION))
        assert(LID.pavement.k_saturated == approx(100, rel=UT_PRECISION))
        assert(LID.pavement.clog_factor == approx(8, rel=UT_PRECISION))
        assert(LID.drain.coefficient == approx(0.5, rel=UT_PRECISION))
        assert(LID.drain.exponent == approx(0.5, rel=UT_PRECISION))
        assert(LID.drain.offset == approx(6, rel=UT_PRECISION))
        assert(LID.drain.delay == approx(6, rel=UT_PRECISION))
        # no drainmat
        assert(LID.drain_mat.thickness == approx(0, rel=UT_PRECISION))
        assert(LID.drain_mat.void_fraction == approx(0, rel=UT_PRECISION))
        assert(LID.drain_mat.roughness == approx(0, rel=UT_PRECISION))
        assert(LID.drain_mat.alpha == approx(0, rel=UT_PRECISION))


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
                assert(sim.current_time.strftime(
                    '%Y-%m-%d %H:%M:%S') == '1998-01-01 05:15:00')
                assert(
                    first_LID_unit_on_sub_2.surface.inflow == approx(
                        0.47, rel=UT_PRECISION))
                assert(
                    first_LID_unit_on_sub_2.evaporation == approx(
                        0, rel=UT_PRECISION))
                assert(
                    first_LID_unit_on_sub_2.surface.infiltration == approx(
                        0.47, rel=UT_PRECISION))
                assert(
                    first_LID_unit_on_sub_2.pavement.percolation == approx(
                        0.47, rel=UT_PRECISION))
                assert(
                    first_LID_unit_on_sub_2.soil.percolation == approx(
                        0.615, rel=UT_PRECISION))
                assert(
                    first_LID_unit_on_sub_2.storage.exfiltration == approx(
                        0, rel=UT_PRECISION))
                assert(
                    first_LID_unit_on_sub_2.surface.outflow == approx(
                        0, rel=UT_PRECISION))
                assert(
                    first_LID_unit_on_sub_2.storage.drain == approx(
                        0, rel=UT_PRECISION))
