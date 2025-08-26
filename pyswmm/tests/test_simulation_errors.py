import pytest
from pyswmm import Simulation

def test_simulation_missing_inp_raises():
    """Simulation should raise an Exception when .inp file is missing."""
    with pytest.raises(Exception) as excinfo:
        with Simulation("this_file_definitely_does_not_exist.inp"):
            pass
    # optional: check error message for clarity
    assert "cannot open input file" in str(excinfo.value).lower()
