# Local imports
from pyswmm import Simulation
from pyswmm import LidControls, LidGroups, LidUnit
from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import MODEL_LIDS_PATH


def test_list_lid_controls():
    with Simulation(MODEL_LIDS_PATH) as sim:
        for control in LidControls(sim):
            print('Global lid control {}'.format(control))
        sim.report()


def test_list_lid_groups():
    with Simulation(MODEL_LIDS_PATH) as sim:
        for group in LidGroups(sim):
            print('subcatchment {} has {} lid units'.format(group,
                                                            len(group)))
            
        sim.report()

def test_list_lid_units():
    with Simulation(MODEL_LIDS_PATH) as sim:
        sub_2_lid_units = LidGroups(sim)["2"]
        for lid_unit in sub_2_lid_units:
            print('subcatchment {} has a lid unit of lid control {}'.format(
                lid_unit.subcatchment,
                lid_unit.lidcontrol))
            
        sim.report()
        
def test_lid_group_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        sub_2_lid_units = LidGroups(sim)["2"]
        
        for step in sim:
            # verify results here
            print(sub_2_lid_units.pervArea)
            print(sub_2_lid_units.flowToPerv)
            print(sub_2_lid_units.oldDrainFlow)
            print(sub_2_lid_units.newDrainFlow)

def test_lid_unit_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        sub_2_lid_units = LidGroups(sim)["2"]

        first_unit = sub_2_lid_units[0]
        # first lid unit defined for "2" subcatchment
        print(first_unit.unitArea)
        print(first_unit.fullWidth)
        print(first_unit.botWidth)
        print(first_unit.initSat)
        print(first_unit.fromImperv)
        print(first_unit.index)
        print(first_unit.number)
        print(first_unit.drainSub)
        print(first_unit.drainNode)
        print(first_unit.total_inflow)
        print(first_unit.total_evap)
        print(first_unit.total_infil)
        print(first_unit.total_surfFlow)
        print(first_unit.total_drainFlow)
        print(first_unit.initVol)
        print(first_unit.finalVol)
        print(first_unit.total_surfDepth)
        print(first_unit.total_paveDepth)
        print(first_unit.soilMoist)
        print(first_unit.total_storDepth)
        print(first_unit.dryTime)
        print(first_unit.oldDrainFlow)
        print(first_unit.newDrainFlow)
        print(first_unit.fluxRate(0))

def test_lid_control_params():
    with Simulation(MODEL_LIDS_PATH) as sim:
        LID = LidControls(sim)["LID"]
        Green_Lid = LidControls(sim)["Green_LID"]

        print("surface")
        print(LID.surface_thickness)
        print(LID.surface_voidFrac)
        print(LID.surface_roughness)
        print(LID.surface_surfSlope)
        print(LID.surface_sideSlope)
        print(LID.surface_alpha)
        print(LID.surface_canOverflow)
        print("soil")
        print(LID.soil_thickness)
        print(LID.soil_porosity)
        print(LID.soil_fieldCap)
        print(LID.soil_wiltPoint)
        print(LID.soil_suction)
        print(LID.soil_kSat)
        print(LID.soil_kSlope)
        print("storage")
        print(LID.storage_thickness)
        print(LID.storage_voidFrac)
        print(LID.storage_kSat)
        print(LID.storage_clogFactor)
        print("pavement")
        print(LID.pavement_thickness)
        print(LID.pavement_voidFrac)
        print(LID.pavement_impervFrac)
        print(LID.pavement_kSat)
        print(LID.pavement_clogFactor)
        print("drain")
        print(LID.drain_coeff)
        print(LID.drain_expon)
        print(LID.drain_offset)
        print(LID.drain_delay)
        print("drainmat")
        print(LID.drainmat_thickness)
        print(LID.drainmat_voidFrac)
        print(LID.drainmat_roughness)
        print(LID.drainmat_alpha)

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
        for step in sim:
            print(sim.current_time)
            print(first_LID_unit_on_sub_2.surface_inflow)
            print(first_LID_unit_on_sub_2.surface_evap)
            print(first_LID_unit_on_sub_2.surface_infil)
            print(first_LID_unit_on_sub_2.pavement_perc)
            print(first_LID_unit_on_sub_2.soil_perc)
            print(first_LID_unit_on_sub_2.storage_exfil)
            print(first_LID_unit_on_sub_2.surface_outflow)
            print(first_LID_unit_on_sub_2.storage_drain)
    
