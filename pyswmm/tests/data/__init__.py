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
MODEL_FULL_FEATURES_PATH = os.path.join(DATA_PATH, 'model_full_features.inp')
MODEL_STORAGE_PUMP = os.path.join(DATA_PATH, 'model_storage_pump.inp')
MODEL_STORAGE_PUMP_MGD = os.path.join(DATA_PATH, 'model_storage_pump_MGD.inp')
MODEL_POLLUTANTS_PATH = os.path.join(DATA_PATH, 'model_pollutants.inp')
WIN_SWMM_LIB_PATH = os.path.join(DATA_PATH, '..\\..\\lib\\windows',
                                 'swmm5.dll')
