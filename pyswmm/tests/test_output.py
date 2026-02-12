# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2025 (See AUTHORS)
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
import pytest

from pyswmm import Simulation
from pyswmm import Output, SubcatchSeries, NodeSeries, LinkSeries, SystemSeries
from pyswmm.tests.data import MODEL_DELAYED_REPORT_PATH, MODEL_WEIR_SETTING_PATH
from pyswmm.errors import OutputException

from swmm.toolkit.shared_enum import (
    LinkAttribute,
    NodeAttribute,
    SubcatchAttribute,
    SystemAttribute,
)
from datetime import datetime, timedelta
from swmm.toolkit import output as tk_output


def test_output_unknown_object_id():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out")) as out:
        with pytest.raises(OutputException):
            flow_rate = out.link_series("C4", LinkAttribute.FLOW_RATE)


def test_output_invalid_time():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out")) as out:
        with pytest.raises(OutputException):
            flow_rate = out.link_series(
                "C3", LinkAttribute.FLOW_RATE, datetime(2015, 10, 1, 15)
            )


def test_output_with():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out")) as out:
        assert len(out.subcatchments) == 3
        assert len(out.nodes) == 5
        assert len(out.links) == 4
        assert len(out.pollutants) == 0

        # access with output methods
        flow_rate = out.link_series("C3", LinkAttribute.FLOW_RATE)
        times = list(flow_rate.keys())
        assert times[0] == datetime(2015, 11, 1, 14, 1)
        assert times[-1] == datetime(2015, 11, 4)
        assert len(flow_rate) == 3480

        subset_flow_rate = out.link_series(
            "C3", LinkAttribute.FLOW_RATE, datetime(2015, 11, 1, 15)
        )
        subset_times = list(subset_flow_rate.keys())
        assert subset_times[0] == datetime(2015, 11, 1, 15)
        assert subset_times[-1] == datetime(2015, 11, 4)

        subset_flow_rate = out.link_series(
            "C3",
            LinkAttribute.FLOW_RATE,
            datetime(2015, 11, 2, 15),
            datetime(2015, 11, 3, 15),
        )
        subset_times = list(subset_flow_rate.keys())
        assert subset_times[0] == datetime(2015, 11, 2, 15)
        assert subset_times[-1] == datetime(2015, 11, 3, 15)

        # Verify end_exclusive=True excludes the end timestep (Python slicing style)
        subset_flow_rate_ex = out.link_series(
            "C3",
            LinkAttribute.FLOW_RATE,
            datetime(2015, 11, 2, 15),
            datetime(2015, 11, 3, 15),
            end_exclusive=True,
        )
        subset_times_ex = list(subset_flow_rate_ex.keys())
        assert subset_times_ex[0] == datetime(2015, 11, 2, 15)
        assert subset_times_ex[-1] == datetime(2015, 11, 3, 14, 59)

        # Also support integer indices with exclusive sentinel stop == len(times)
        all_series_ex = out.link_series(
            "C3", LinkAttribute.FLOW_RATE, 0, len(out.times), end_exclusive=True
        )
        all_times_ex = list(all_series_ex.keys())
        assert all_times_ex[0] == out.times[0]
        assert all_times_ex[-1] == out.times[-1]
        assert len(all_series_ex) == len(out.times)

        assert len(out.node_series("J1", NodeAttribute.TOTAL_INFLOW)) == 3480
        assert len(out.subcatch_series("S1", SubcatchAttribute.RUNOFF_RATE)) == 3480
        assert len(out.system_series(SystemAttribute.EVAP_INFIL_LOSS)) == 3480

        assert len(out.subcatch_attribute(SubcatchAttribute.RUNOFF_RATE, 0)) == 3
        assert len(out.node_attribute(NodeAttribute.HYDRAULIC_HEAD, 0)) == 5
        assert len(out.link_attribute(LinkAttribute.FLOW_RATE, 0)) == 4
        # waiting for function to be fixed
        # assert len(out.system_attribute('air_temp', 0)) == 1

        # no pollutant
        assert len(out.subcatch_result("S1", 0)) == len(SubcatchAttribute) - 1
        assert len(out.node_result("J1", 0)) == len(NodeAttribute) - 1
        assert len(out.link_result("C1", 0)) == len(LinkAttribute) - 1
        assert len(out.system_result(0)) == len(SystemAttribute)


def test_output():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    out = Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out"))
    out.open()
    assert len(out.subcatchments) == 3
    assert len(out.nodes) == 5
    assert len(out.links) == 4
    assert len(out.pollutants) == 0
    flow_rate = out.link_series("C3", "flow_rate")
    times = list(flow_rate.keys())
    assert times[0] == datetime(2015, 11, 1, 14, 1)
    assert times[-1] == datetime(2015, 11, 4)
    assert len(flow_rate) == 3480
    out.close()


def test_timeseries_abstraction():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out")) as out:
        for attr in SubcatchAttribute:
            series = getattr(SubcatchSeries(out)["S1"], attr.name.lower())
            assert len(series) == 3480
        for attr in NodeAttribute:
            series = getattr(NodeSeries(out)["J1"], attr.name.lower())
            assert len(series) == 3480
        for attr in LinkAttribute:
            series = getattr(LinkSeries(out)["C1:C2"], attr.name.lower())
            assert len(series) == 3480
        for attr in SystemAttribute:
            series = getattr(SystemSeries(out), attr.name.lower())
            assert len(series) == 3480


def test_times_loaded_from_binary():
    # Run the model to produce the .out
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    # Verify out.times equals toolkit-decoded date series
    with Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out")) as out:
        raw = tk_output.get_date_series(out.handle, 0, out.period - 1)
        decoded = [
            datetime(*tk_output.decode_date(d)[:6]).replace(microsecond=0) for d in raw
        ]
        assert out.times == decoded


def test_times_sequence_properties():
    # Produce the output file
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for _ in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out")) as out:
        times = out.times

        # Basic properties
        assert isinstance(times, list)
        assert len(times) == out.period
        assert all(t.microsecond == 0 for t in times)

        # Start time is non-inclusive; index 0 is rpt_start + rpt_step
        assert times[0] == (out.rpt_start + timedelta(seconds=out.rpt_step))

        # Last timestamp equals end (end inclusive)
        assert times[-1] == out.end

        # Monotonic with constant step equal to report seconds
        step_secs = [
            (times[i + 1] - times[i]).total_seconds() for i in range(len(times) - 1)
        ]
        assert all(s == out.rpt_step for s in step_secs)


def test_delayed_start_sequence_props():
    # Produce the output file
    with Simulation(MODEL_DELAYED_REPORT_PATH) as sim:
        for _ in sim:
            pass

    with Output(MODEL_DELAYED_REPORT_PATH.replace("inp", "out")) as out:
        times = out.times

        # Basic properties
        assert isinstance(times, list)
        assert len(times) == out.period
        assert all(t.microsecond == 0 for t in times)

        # Start time is non-inclusive; index 0 is rpt_start + rpt_step
        assert times[0] == (out.rpt_start + timedelta(seconds=out.rpt_step))

        # Last timestamp equals end (end inclusive)
        assert times[-1] == out.end

        # Monotonic with constant step equal to report seconds
        step_secs = [
            (times[i + 1] - times[i]).total_seconds() for i in range(len(times) - 1)
        ]
        assert all(s == out.rpt_step for s in step_secs)


def test_verify_time_binary_search_datetime():
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for step in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out")) as out:
        # Pick a middle timestamp and ensure verify_time finds it
        mid = len(out.times) // 2
        dt = out.times[mid]
        idx = Output.verify_time(dt, out.times, out.rpt_start, out.end, out.rpt_step, 0)
        assert idx == mid
        # None defaults to 0
        assert (
            Output.verify_time(None, out.times, out.rpt_start, out.end, out.rpt_step, 0)
            == 0
        )


def test_verify_time_datetime_before_start():
    # Produce output
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for _ in sim:
            pass

    # Verify a timestamp equal to model start is rejected (not a reporting time)
    with Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out")) as out:
        bad_dt = out.rpt_start
        with pytest.raises(OutputException) as exc:
            Output.verify_time(
                bad_dt, out.times, out.rpt_start, out.end, out.rpt_step, 0
            )
        assert "does not exist in model output reporting time steps." in str(exc.value)


def test_verify_time():
    # Produce the output file (simulation start != report start)
    with Simulation(MODEL_WEIR_SETTING_PATH) as sim:
        for _ in sim:
            pass

    with Output(MODEL_WEIR_SETTING_PATH.replace("inp", "out")) as out:
        # Times are aligned to report step and built from the binary
        assert isinstance(out.times, list)
        assert len(out.times) == out.period

        temp_out = out.node_series("J2", NodeAttribute.TOTAL_INFLOW)
        assert len(temp_out) == out.period

        # Non-inclusive start: index 0 == (report_start + report)
        assert out.times[0] == out.rpt_start + timedelta(seconds=out.rpt_step)
        assert out.times[-1] == out.end

        # Requesting the (non-inclusive) report start should fail with a clear message
        with pytest.raises(OutputException):
            temp_out = out.node_series(
                "J2", NodeAttribute.TOTAL_INFLOW, out.rpt_start, out.end
            )

        # verify_time returns indices for valid datetimes
        assert (
            Output.verify_time(
                out.times[0], out.times, out.rpt_start, out.end, out.rpt_step, 0
            )
            == 0
        )
        assert (
            Output.verify_time(
                out.times[-1], out.times, out.rpt_start, out.end, out.rpt_step, 0
            )
            == len(out.times) - 1
        )

        # Requesting the (non-inclusive) report start should fail with a clear message
        implied_report_start = out.times[0] - timedelta(seconds=out.rpt_step)
        with pytest.raises(OutputException) as exc:
            Output.verify_time(
                implied_report_start, out.times, out.rpt_start, out.end, out.rpt_step, 0
            )
        msg = str(exc.value).lower()
        assert "does not exist" in msg  # or "index 0" in msg

        # Non-aligned datetime between start and first reporting time should fail
        bad_dt = implied_report_start + timedelta(seconds=1)
        with pytest.raises(OutputException):
            Output.verify_time(
                bad_dt, out.times, out.rpt_start, out.end, out.rpt_step, 0
            )


def test_verify_time_with_report_delay():
    # Produce the output file (simulation start != report start)
    with Simulation(MODEL_DELAYED_REPORT_PATH) as sim:
        for _ in sim:
            pass

    with Output(MODEL_DELAYED_REPORT_PATH.replace("inp", "out")) as out:
        # Times are aligned to report step and built from the binary
        assert isinstance(out.times, list)
        assert len(out.times) == out.period

        temp_out = out.node_series("J2", NodeAttribute.TOTAL_INFLOW)
        assert len(temp_out) == out.period

        # Non-inclusive start: index 0 == (report_start + report)
        assert out.times[0] == out.rpt_start + timedelta(seconds=out.rpt_step)
        assert out.times[-1] == out.end

        # Requesting the (non-inclusive) report start should fail with a clear message
        with pytest.raises(OutputException):
            temp_out = out.node_series(
                "J2", NodeAttribute.TOTAL_INFLOW, out.rpt_start, out.end
            )

        # verify_time returns indices for valid datetimes
        assert (
            Output.verify_time(
                out.times[0], out.times, out.rpt_start, out.end, out.rpt_step, 0
            )
            == 0
        )
        assert (
            Output.verify_time(
                out.times[-1], out.times, out.rpt_start, out.end, out.rpt_step, 0
            )
            == len(out.times) - 1
        )

        # Requesting the (non-inclusive) report start should fail with a clear message
        implied_report_start = out.times[0] - timedelta(seconds=out.rpt_step)
        with pytest.raises(OutputException) as exc:
            Output.verify_time(
                implied_report_start, out.times, out.rpt_start, out.end, out.rpt_step, 0
            )
        msg = str(exc.value).lower()
        assert "does not exist" in msg  # or "index 0" in msg

        # Non-aligned datetime between start and first reporting time should fail
        bad_dt = implied_report_start + timedelta(seconds=1)
        with pytest.raises(OutputException):
            Output.verify_time(
                bad_dt, out.times, out.rpt_start, out.end, out.rpt_step, 0
            )
