# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2025 (See AUTHORS)
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

import pytest
from pyswmm import Simulation, Output


@pytest.mark.parametrize("cls", [Simulation])
def test_path_argument_type_errors_simulation(cls):
    """Simulation should reject clearly invalid path-like argument types."""
    with pytest.raises((TypeError, AttributeError, ValueError, Exception)):
        cls(object())  # nonsense argument
