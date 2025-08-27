import re
import pyswmm


def test_public_imports_exist():
    """Public API objects mentioned in docs should be importable."""
    from pyswmm import Simulation, Nodes, Links, Output  # noqa: F401


def test_version_semverish():
    """__version__ should look like semantic versioning."""
    ver = getattr(pyswmm, "__version__", "")
    assert re.match(r"^\d+\.\d+\.\d+", str(ver)) is not None
