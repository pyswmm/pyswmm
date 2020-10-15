import pytest
import warnings
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH


def test_import_from_simulation():
    with pytest.warns(None) as record:
        from pyswmm import Links, Nodes, Simulation
        sim = Simulation(MODEL_WEIR_SETTING_PATH)
    assert not record


def test_import_from_swmm5():
    from pyswmm.swmm5 import PySWMM
    sim = PySWMM(MODEL_WEIR_SETTING_PATH)
