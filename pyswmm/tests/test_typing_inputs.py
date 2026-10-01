# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2025 (See AUTHORS)
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

import pytest
from pyswmm import Simulation, Output
from pyswmm.swmm5 import PySWMM, solver


@pytest.mark.parametrize("argument", ["inputfile", "reportfile", "outputfile"])
def test_path_argument_type_errors_simulation(monkeypatch, argument):
    """Simulation should reject clearly invalid path-like argument types."""
    calls = []
    monkeypatch.setattr(solver, "swmm_open", lambda *args: calls.append("open"))
    monkeypatch.setattr(solver, "swmm_close", lambda: calls.append("close"))
    arguments = {"inputfile": "model.inp", argument: object()}
    with pytest.raises((TypeError, AttributeError)):
        Simulation(**arguments)
    assert calls == []


@pytest.mark.parametrize("close_fails", [False, True])
def test_native_open_failure_preserves_error(monkeypatch, close_fails):
    original = RuntimeError("open failure")
    calls = []

    def fail_open(*args):
        calls.append("open")
        raise original

    def close():
        calls.append("close")
        if close_fails:
            raise RuntimeError("close failure")

    monkeypatch.setattr(solver, "swmm_open", fail_open)
    monkeypatch.setattr(solver, "swmm_close", close)
    model = PySWMM("model.inp")
    with pytest.raises(RuntimeError) as caught:
        model.swmm_open()
    assert caught.value is original
    assert calls == ["open", "close"]
    assert not model.fileLoaded
