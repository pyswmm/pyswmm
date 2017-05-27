# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""SWMM5 test models."""

# Standard library imports
import os

DATA_PATH = os.path.abspath(os.path.dirname(__file__))

# Test models paths
MODEL_NODE_INFLOWS_PATH = os.path.join(DATA_PATH, 'model_node_inflows.inp')
MODEL_PUMP_SETTINGS_PATH = os.path.join(DATA_PATH, 'model_pump_setting.inp')
MODEL_TOOLKIT_UNITS_PATH = os.path.join(DATA_PATH, 'model_toolkit_units.inp')
MODEL_WEIR_SETTING_PATH = os.path.join(DATA_PATH, 'model_weir_setting.inp')

# Images
IMAGE_NODE_INFLOWS_PATH = os.path.join(DATA_PATH, 'node_inflows.PNG')
IMAGE_WEIR_SETTING_PATH = os.path.join(DATA_PATH, 'weir_setting.PNG')

