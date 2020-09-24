import pytest
import warnings

from pyswmm.error import SWMM5FutureWarning


def test_import_from_swmm5():
    with pytest.warns(SWMM5FutureWarning):
        from pyswmm.swmm5 import SWMMException


def test_import_from_simulation():
    with pytest.warns(None) as record:
        from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH
        from pyswmm import Links, Nodes, Simulation
        sim = Simulation(MODEL_WEIR_SETTING_PATH)
    assert not record
