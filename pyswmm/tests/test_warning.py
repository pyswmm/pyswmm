import pytest
import warnings

from pyswmm.error import SWMM5FutureWarning


def test_import_from_simulation():
    with pytest.warns(None) as record:
        from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH
        from pyswmm import Links, Nodes, Simulation
        sim = Simulation(MODEL_WEIR_SETTING_PATH)
    assert not record
