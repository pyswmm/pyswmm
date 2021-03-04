import pytest
from pyswmm import Simulation
from pyswmm.errors import IncompleteSimulation
from pyswmm.tests.data import MODEL_FULL_FEATURES_PATH


def test_error_incomplete_sim():
    with pytest.raises(IncompleteSimulation):
        with Simulation(MODEL_FULL_FEATURES_PATH) as sim:
            sim.output.open()
