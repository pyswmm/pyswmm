from pyswmm import Simulation, Output
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_simulation_output_with():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out')) as out:
        pass
        # access with output methods
test_simulation_output_with()

def test_simulation_output():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    output = Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out'))
    output.open()
    output.close()