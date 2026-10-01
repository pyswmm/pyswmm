# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2025 (See AUTHORS)
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
import pickle
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent

import pytest
from swmm.toolkit import output as tk_output
from swmm.toolkit import output as toolkit_output
from swmm.toolkit.shared_enum import (
    LinkAttribute,
    NodeAttribute,
    SubcatchAttribute,
    SystemAttribute,
)

from pyswmm import (
    LinkSeries,
    NodeSeries,
    Output,
    Simulation,
    SubcatchSeries,
    SystemSeries,
)
from pyswmm._monkey_patch import ToolkitVersionException
from pyswmm.errors import OutputException
from pyswmm.tests.data import (
    MODEL_DELAYED_REPORT_PATH,
    MODEL_POLLUTANTS_PATH,
    MODEL_WEIR_SETTING_PATH,
)


@pytest.fixture(scope="module")
def pollutant_output_files(tmp_path_factory):
    directory = tmp_path_factory.mktemp("pollutant_output")
    files = {}
    for count in (0, 1, 3):
        source = Path(
            MODEL_POLLUTANTS_PATH if count else MODEL_WEIR_SETTING_PATH
        ).read_text()
        if count == 3:
            source = source.replace(
                "[LANDUSES]",
                "second-pollutant MG/L 20 0 0 0 NO * 0 0 0\n"
                "third-pollutant MG/L 30 0 0 0 NO * 0 0 0\n\n[LANDUSES]",
            )
        filename = directory / "model_{}.inp".format(count)
        filename.write_text(source)
        with Simulation(str(filename)) as sim:
            for _ in sim:
                pass
        files[count] = str(filename.with_suffix(".out"))
    return files


@pytest.mark.parametrize("count", [0, 1, 3])
@pytest.mark.parametrize(
    "kind,base_enum,series_class",
    [
        ("subcatch", SubcatchAttribute, SubcatchSeries),
        ("node", NodeAttribute, NodeSeries),
        ("link", LinkAttribute, LinkSeries),
    ],
)
def test_output_all_pollutants(
    pollutant_output_files, count, kind, base_enum, series_class
):
    original_members = dict(base_enum.__members__)
    with Output(pollutant_output_files[count]) as out:
        result = getattr(out, f"{kind}_result")(0, 0)
        raw_result = getattr(toolkit_output, f"get_{kind}_result")(out.handle, 0, 0)
        assert len(result) == len(raw_result)
        assert list(result.values()) == pytest.approx(raw_result)

        assert pickle.loads(pickle.dumps(result)) == result
        attributes = getattr(out, f"{kind}_attributes")
        first_pollutant = base_enum.POLLUT_CONC_0.value
        expected_names = [m.name for m in base_enum if m.value < first_pollutant]
        expected_names += [f"POLLUT_CONC_{i}" for i in range(count)]
        assert list(attributes) == expected_names
        assert [member.name for member in result] == expected_names
        assert list(result) == list(attributes.values())
        for name, member in original_members.items():
            if name in attributes:
                assert attributes[name] is member

        series = series_class(out)[0]
        for index in range(count):
            name = f"POLLUT_CONC_{index}"
            attribute = attributes[name]
            # Read complete raw rows so the reference does not rely on the
            # same attribute-enum conversion as the methods under test.
            raw_series = [
                getattr(toolkit_output, f"get_{kind}_result")(out.handle, period, 0)[
                    first_pollutant + index
                ]
                for period in range(out.period)
            ]
            expected = dict(zip(out.times, raw_series))
            assert getattr(out, f"{kind}_series")(0, attribute) == expected
            assert getattr(series, name.lower()) == expected
            assert name.lower() in dir(series)
            # Exercise snapshots during a nonzero concentration, not just the
            # initially dry report where different pollutants can all be zero.
            report_index = max(range(out.period), key=raw_series.__getitem__)
            assert raw_series[report_index] > 0
            at_time = getattr(out, f"{kind}_attribute")(attribute, report_index)
            assert list(at_time.values())[0] == pytest.approx(raw_series[report_index])
        with pytest.raises(AttributeError):
            getattr(series, f"pollut_conc_{count}")
        assert f"pollut_conc_{count}" not in dir(series)
    assert base_enum.__members__ == original_members


def test_output_pollutant_attributes_are_isolated(pollutant_output_files):
    with (
        Output(pollutant_output_files[3]) as multiple,
        Output(pollutant_output_files[0]) as none,
        Output(pollutant_output_files[1]) as single,
    ):
        for kind in ("subcatch", "node", "link"):
            name = f"{kind}_attributes"
            multiple_attributes = getattr(multiple, name)
            assert "POLLUT_CONC_2" in multiple_attributes
            assert "POLLUT_CONC_0" not in getattr(none, name)
            assert "POLLUT_CONC_1" not in getattr(single, name)
            assert getattr(multiple, name) is multiple_attributes


@pytest.mark.parametrize("toolkit_version", ["0.9.1", "0.16.2", "0.17.0rc1"])
def test_output_rejects_unsupported_toolkit(monkeypatch, toolkit_version):
    monkeypatch.setattr("pyswmm.output._tk_version", toolkit_version)

    with pytest.raises(ToolkitVersionException) as error:
        Output("model.out")

    assert "swmm-toolkit>=0.17.0" in str(error.value)
    assert toolkit_version in str(error.value)


@pytest.mark.parametrize("toolkit_version", ["0.17.0", "0.17.1", "0.100.0", "1.0.0"])
def test_output_accepts_supported_toolkit(monkeypatch, toolkit_version):
    monkeypatch.setattr("pyswmm.output._tk_version", toolkit_version)

    out = Output("model.out")

    assert out.binfile == "model.out"
    assert out.handle is None
    assert not out.loaded


@pytest.mark.parametrize("kind", ["missing", "directory"])
@pytest.mark.parametrize("access", ["open", "context", "property"])
def test_output_unreadable_path(tmp_path, kind, access):
    path = tmp_path / "unreadable.out"
    if kind == "directory":
        path.mkdir()
    # An invalid filename can crash the native library, so isolate this
    # regression rather than allowing a crash to terminate the whole suite.
    script = dedent(
        """\
        import sys
        from pyswmm import Output

        path, access = sys.argv[1:]
        out = Output(path)
        try:
            if access == "open":
                out.open()
            elif access == "context":
                with out:
                    pass
            else:
                out.project_size
        except OSError as error:
            assert error.filename == path
            assert not out.loaded
            assert out.handle is None
            assert out.close()
        else:
            raise AssertionError("An unreadable output path must raise OSError")
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", script, str(path), access],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_output_retry_after_missing_file(tmp_path):
    model = tmp_path / "model.inp"
    model.write_text(Path(MODEL_WEIR_SETTING_PATH).read_text())
    with Simulation(str(model)) as sim:
        for _ in sim:
            pass
    script = dedent(
        """\
        import shutil
        import sys
        from unittest.mock import patch
        from pyswmm import Output
        from swmm.toolkit.shared_enum import NodeAttribute

        source, destination = sys.argv[1:]
        out = Output(destination)
        try:
            out.open()
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("Expected a missing-file error")
        shutil.copyfile(source, destination)
        with out:
            assert out.loaded
            assert len(out.nodes) > 0
            assert len(out.node_series(0, NodeAttribute.HYDRAULIC_HEAD)) == out.period
            # An already-open reader does not need to open the file again.
            with patch("builtins.open", side_effect=AssertionError):
                assert out.open()
        assert not out.loaded
        """
    )
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(model.with_suffix(".out")),
            str(tmp_path / "later.out"),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


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
        for attr in out.subcatch_attributes.values():
            series = getattr(SubcatchSeries(out)["S1"], attr.name.lower())
            assert len(series) == 3480
        for attr in out.node_attributes.values():
            series = getattr(NodeSeries(out)["J1"], attr.name.lower())
            assert len(series) == 3480
        for attr in out.link_attributes.values():
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


def test_verify_time_rejects_bool_index():
    base = datetime(2020, 1, 1, 0, 1)
    times = [base + timedelta(minutes=i) for i in range(3)]
    start = base - timedelta(minutes=1)
    end = times[-1]

    with pytest.raises(OutputException):
        Output.verify_time(True, times, start, end, 60, 0)

    with pytest.raises(OutputException):
        Output.verify_time(False, times, start, end, 60, 0)


def test_verify_time_empty_time_list_raises():
    with pytest.raises(OutputException) as exc:
        Output.verify_time(
            datetime(2020, 1, 1, 0, 1),
            [],
            datetime(2020, 1, 1, 0, 0),
            datetime(2020, 1, 1, 0, 2),
            60,
            0,
        )

    assert "contains no reporting time steps" in str(exc.value).lower()


def test_verify_time_honors_start_end_bounds():
    base = datetime(2020, 1, 1, 0, 1)
    times = [base + timedelta(minutes=i) for i in range(3)]

    # Start excludes first element even if present in time_list
    with pytest.raises(OutputException):
        Output.verify_time(times[0], times, times[1], times[-1], 60, 0)

    # End excludes last element if configured earlier than time_list max
    with pytest.raises(OutputException):
        Output.verify_time(times[-1], times, times[0], times[1], 60, 0)
