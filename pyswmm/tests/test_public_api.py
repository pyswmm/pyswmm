# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2025 (See AUTHORS)
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

import re
import pyswmm


def test_public_imports_exist():
    """Public API objects mentioned in docs should be importable."""
    from pyswmm import Simulation, Nodes, Links, Output  # noqa: F401


def test_version_semverish():
    """__version__ should look like semantic versioning."""
    ver = getattr(pyswmm, "__version__", "")
    assert re.match(r"^\d+\.\d+\.\d+", str(ver)) is not None
