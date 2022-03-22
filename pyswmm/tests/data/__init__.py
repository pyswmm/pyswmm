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
import sys
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
MODEL_POLLUTANTS_PATH_2 = os.path.join(DATA_PATH, 'model_pollutants_2.inp')
MODEL_POLLUTANTS_SETTERS_PATH = os.path.join(DATA_PATH, 'model_pollutants_setters.inp')
MODEL_RAIN = os.path.join(DATA_PATH, 'model_rain.inp')
MODEL_LIDS_PATH = os.path.join(DATA_PATH, 'model_lids.inp')
MODEL_BAD_INPUT_PATH_1 = os.path.join(DATA_PATH, 'model_bad_input_1.inp')
MODEL_SUBCATCH_STATS_PATH = os.path.join(DATA_PATH, 'model_subcatch_stats.inp')

WIN_SWMM_LIB_PATH = os.path.join(DATA_PATH, '..\\..\\lib\\windows',
                                 'swmm5.dll')
if sys.maxsize > 2**32:
    WIN_SWMM_LIB_PATH = os.path.join(DATA_PATH, '..\\..\\lib\\windows',
                                     'swmm5-x64.dll')
else:
    WIN_SWMM_LIB_PATH = os.path.join(DATA_PATH, '..\\..\\lib\\windows',
                                     'swmm5.dll')
