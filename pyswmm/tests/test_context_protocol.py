from pyswmm import Simulation, Output

def test_simulation_context_protocol():
    """Simulation should implement context manager protocol."""
    assert hasattr(Simulation, "__enter__")
    assert hasattr(Simulation, "__exit__")
    assert callable(Simulation.__enter__)
    assert callable(Simulation.__exit__)

def test_output_context_protocol():
    """Output should implement context manager protocol."""
    assert hasattr(Output, "__enter__")
    assert hasattr(Output, "__exit__")
    assert callable(Output.__enter__)
    assert callable(Output.__exit__)
