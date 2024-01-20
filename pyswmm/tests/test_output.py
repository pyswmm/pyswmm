# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2021 Jennifer Wu
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
import pytest

from pyswmm import Simulation
from pyswmm import Output, SubcatchSeries, NodeSeries, LinkSeries, SystemSeries
from pyswmm.tests.data import MODEL_WEIR_SETTING_PATH
from pyswmm.errors import OutputException

from swmm.toolkit.shared_enum import LinkAttribute, NodeAttribute, SubcatchAttribute, SystemAttribute
from datetime import datetime


def test_output_unknown_object_id():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out')) as out:
        with pytest.raises(OutputException):
            flow_rate = out.link_series('C4', LinkAttribute.FLOW_RATE)


def test_output_invalid_time():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out')) as out:
        with pytest.raises(OutputException):
            flow_rate = out.link_series(
                'C3', LinkAttribute.FLOW_RATE, datetime(
                    2015, 10, 1, 15))


def test_output_with():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out')) as out:
        assert len(out.subcatchments) == 3
        assert len(out.nodes) == 5
        assert len(out.links) == 4
        assert len(out.pollutants) == 0

        # access with output methods
        flow_rate = out.link_series('C3', LinkAttribute.FLOW_RATE)
        times = list(flow_rate.keys())
        assert times[0] == datetime(2015, 11, 1, 14, 1)
        assert times[-1] == datetime(2015, 11, 4)
        assert len(flow_rate) == 3480

        subset_flow_rate = out.link_series(
            'C3', LinkAttribute.FLOW_RATE, datetime(
                2015, 11, 1, 15))
        subset_times = list(subset_flow_rate.keys())
        assert subset_times[0] == datetime(2015, 11, 1, 15)
        assert subset_times[-1] == datetime(2015, 11, 4)

        subset_flow_rate = out.link_series(
            'C3', LinkAttribute.FLOW_RATE, datetime(
                2015, 11, 2, 15), datetime(
                2015, 11, 3, 15))
        subset_times = list(subset_flow_rate.keys())
        assert subset_times[0] == datetime(2015, 11, 2, 15)
        assert subset_times[-1] == datetime(2015, 11, 3, 14, 59)

        assert len(out.node_series('J1', NodeAttribute.TOTAL_INFLOW)) == 3480
        assert len(
            out.subcatch_series(
                'S1',
                SubcatchAttribute.RUNOFF_RATE)) == 3480
        assert len(out.system_series(SystemAttribute.EVAP_INFIL_LOSS)) == 3480

        assert len(
            out.subcatch_attribute(
                SubcatchAttribute.RUNOFF_RATE,
                0)) == 3
        assert len(out.node_attribute(NodeAttribute.HYDRAULIC_HEAD, 0)) == 5
        assert len(out.link_attribute(LinkAttribute.FLOW_RATE, 0)) == 4
        # waiting for function to be fixed
        # assert len(out.system_attribute('air_temp', 0)) == 1

        # no pollutant
        assert len(out.subcatch_result('S1', 0)) == len(SubcatchAttribute) - 1
        assert len(out.node_result('J1', 0)) == len(NodeAttribute) - 1
        assert len(out.link_result('C1', 0)) == len(LinkAttribute) - 1
        assert len(out.system_result(0)) == len(SystemAttribute)


def test_output():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    out = Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out'))
    out.open()
    assert len(out.subcatchments) == 3
    assert len(out.nodes) == 5
    assert len(out.links) == 4
    assert len(out.pollutants) == 0
    flow_rate = out.link_series('C3', 'flow_rate')
    times = list(flow_rate.keys())
    assert times[0] == datetime(2015, 11, 1, 14, 1)
    assert times[-1] == datetime(2015, 11, 4)
    assert len(flow_rate) == 3480
    out.close()


def test_timeseries_abstraction():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace('inp', 'out')) as out:
        for attr in SubcatchAttribute:
            series = getattr(SubcatchSeries(out)['S1'], attr.name.lower())
            assert len(series) == 3480
        for attr in NodeAttribute:
            series = getattr(NodeSeries(out)['J1'], attr.name.lower())
            assert len(series) == 3480
        for attr in LinkAttribute:
            series = getattr(LinkSeries(out)['C1:C2'], attr.name.lower())
            assert len(series) == 3480
        for attr in SystemAttribute:
            series = getattr(SystemSeries(out), attr.name.lower())
            assert len(series) == 3480
