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
                                                            len(group)) == 'subcatchment 2 has 2 lid units')
            if i == 2:
                assert('subcatchment {} has {} lid units'.format(group,
                                                            len(group)) == 'subcatchment 3 has 0 lid units')
            if i == 3:
                assert('subcatchment {} has {} lid units'.format(group,
                                                            len(group)) == 'subcatchment 4 has 0 lid units')
            if i == 7:
                assert('subcatchment {} has {} lid units'.format(group,
                                                            len(group)) == 'subcatchment 8 has 0 lid units')
        #sim.report()

def test_list_lid_units():
    with Simulation(MODEL_LIDS_PATH) as sim:
        sub_2_lid_units = LidGroups(sim)["2"]
        for i, lid_unit in enumerate(sub_2_lid_units):
            if i == 0:
                assert(lid_unit.subcatchment == '2')
                assert(lid_unit.lidcontrol == 'LID')
            if i == 1:
                assert(lid_unit.subcatchment == '2')
                assert(lid_unit.lidcontrol == 'Green_LID')
        
def test_lid_group_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        sub_2_lid_units = LidGroups(sim)["2"]
        sim.step_advance(900)
        for i, step in enumerate(sim):
            # verify results here
            if i == 115:
                assert(sim.current_time.strftime('%Y-%m-%d %H:%M:%S') == '1998-01-02 05:00:00')
                assert(sub_2_lid_units.pervArea == 50000)
                assert(round(sub_2_lid_units.flowToPerv, 4) == 0.2683)
                assert(round(sub_2_lid_units.oldDrainFlow, 4) == 0)
                assert(round(sub_2_lid_units.newDrainFlow, 4) == 0)

def test_lid_unit_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        sub_2_lid_units = LidGroups(sim)["2"]
        first_unit = sub_2_lid_units[0]
        assert(first_unit.unitArea == 10000)
        assert(first_unit.fullWidth == 20)
        assert(first_unit.initSat == 0)
        assert(first_unit.fromImperv == 50)
        assert(first_unit.index == 0)
        assert(first_unit.number == 4)
        assert(first_unit.drainSub == -1)
        assert(first_unit.drainNode == 1)

        for i, step in enumerate(sim):
            if i == 2145:
                assert(round(first_unit.total_inflow, 4) == 8.9917)
                assert(first_unit.total_evap == 0)
                assert(round(first_unit.total_infil, 4) == 0.0142)
                assert(first_unit.total_surfFlow == 0)
                assert(round(first_unit.total_drainFlow, 4) == 3.4058)
                assert(first_unit.initVol == 3)
                assert(round(first_unit.finalVol, 4) == 8.5717)
                assert(first_unit.total_surfDepth == 0)
                assert(first_unit.total_paveDepth == 0)
                assert(round(first_unit.soilMoist, 4) == 0.2)
                assert(round(first_unit.total_storDepth, 4) == 6.0003)
                assert(first_unit.dryTime == 21600)
                assert(first_unit.oldDrainFlow == 0)
                assert(first_unit.newDrainFlow == 0)
                assert(first_unit.fluxRate(0) == 0)

def test_lid_control_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        LID = LidControls(sim)["LID"]
        Green_Lid = LidControls(sim)["Green_LID"]

        assert(LID.surface_thickness == 10)
        assert(LID.surface_voidFrac == 0.5)
        assert(LID.surface_roughness == 0.013)
        assert(LID.surface_surfSlope == 1)
        assert(LID.surface_sideSlope == 5)
        assert(round(LID.surface_alpha, 4) == 11.4615)
        assert(LID.surface_canOverflow == False)
        assert(LID.soil_thickness == 30)
        assert(LID.soil_porosity == 0.5)
        assert(LID.soil_fieldCap == 0.2)
        assert(LID.soil_wiltPoint == 0.1)
        assert(LID.soil_suction == 3.5)
        assert(LID.soil_kSat == 5.0)
        assert(LID.soil_kSlope == 10)
        assert(LID.storage_thickness == 40)
        assert(round(LID.storage_voidFrac, 4) == 0.75)
        assert(LID.storage_kSat == 0.5)
        assert(LID.storage_clogFactor == 0.2)
        assert(LID.pavement_thickness == 20)
        assert(round(LID.pavement_voidFrac, 4) == 0.15)
        assert(LID.pavement_impervFrac == 0.5)
        assert(LID.pavement_kSat == 100)
        assert(LID.pavement_clogFactor == 8)
        assert(LID.drain_coeff == 0.5)
        assert(LID.drain_expon == 0.5)
        assert(LID.drain_offset == 6)
        assert(LID.drain_delay == 6)
        # no drainmat
        assert(LID.drainmat_thickness == 0)
        assert(LID.drainmat_voidFrac == 0)
        assert(LID.drainmat_roughness == 0)
        assert(LID.drainmat_alpha == 0)

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
                assert(round(first_LID_unit_on_sub_2.surface_inflow, 4) == 0.4778)
                assert(round(first_LID_unit_on_sub_2.surface_evap, 4) == 0)
                assert(round(first_LID_unit_on_sub_2.surface_infil, 4) == 0.4778)
                assert(round(first_LID_unit_on_sub_2.pavement_perc, 4) == 0.4778)
                assert(round(first_LID_unit_on_sub_2.soil_perc, 4) == 0.6203)
                assert(round(first_LID_unit_on_sub_2.storage_exfil, 4) == 0)
                assert(round(first_LID_unit_on_sub_2.surface_outflow, 4) == 0)
                assert(round(first_LID_unit_on_sub_2.storage_drain, 4) == 0)

