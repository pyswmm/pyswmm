import pytest
from pyswmm import Output
from pyswmm.errors import OutputException

def test_output_missing_file_raises_clean_error():
    """Opening a non-existent .out should raise a Python exception (no segfault)."""
    with pytest.raises(OutputException):
        with Output("this_file_does_not_exist_123456.out"):
            pass
