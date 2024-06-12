# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Pytest fixtures and helpers."""


def get_model_files(name):
    """Return the input, report and output name based on the input name."""
    base_name = name.split(".inp")[0]
    report_name = base_name + ".rpt"
    output_name = base_name + ".out"
    return name, report_name, output_name
