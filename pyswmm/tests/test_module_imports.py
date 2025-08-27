import importlib


def test_submodules_importable_without_side_effects():
    """Selected submodules should import without requiring SWMM runtime."""
    # These imports should not execute a simulation nor require binaries
    for name in ("pyswmm.nodes", "pyswmm.links", "pyswmm.simulation", "pyswmm.output"):
        mod = importlib.import_module(name)
        assert mod is not None
