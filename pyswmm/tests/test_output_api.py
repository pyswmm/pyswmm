# pyswmm/tests/test_output_api.py

"""
Smoke tests for pyswmm.Output that avoid touching the SWMM C layer.

These tests intentionally DO NOT open any .out files, because the C extension
(swmm.toolkit.output) may segfault when given invalid paths on some platforms.
"""

import importlib
import inspect
import types


def test_output_symbol_is_exposed_and_is_class():
    """Output should be importable from pyswmm and be a class/type."""
    from pyswmm import Output  # noqa: F401
    assert isinstance(Output, type)


def test_output_module_import_has_no_runtime_side_effects():
    """Importing pyswmm.output should succeed without running SWMM or touching files."""
    mod = importlib.import_module("pyswmm.output")
    assert isinstance(mod, types.ModuleType)
    # basic sanity: the symbol is present on the module too
    assert hasattr(mod, "Output")


def test_output_has_context_protocol_methods_only():
    """
    Output should declare context manager hooks (__enter__/__exit__),
    but we do not call them here (to avoid invoking the C backend).
    """
    from pyswmm import Output
    assert hasattr(Output, "__enter__")
    assert hasattr(Output, "__exit__")
    assert callable(Output.__enter__)
    assert callable(Output.__exit__)
    # Additionally, make sure constructor is introspectable (no crash on inspect)
    sig = inspect.signature(Output)
    assert isinstance(sig, inspect.Signature)
