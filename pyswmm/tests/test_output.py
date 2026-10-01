# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2025 (See AUTHORS)
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
import pickle
import pytest
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

from pyswmm import Simulation
from pyswmm import Output, SubcatchSeries, NodeSeries, LinkSeries, SystemSeries
from pyswmm.tests.data import MODEL_POLLUTANTS_PATH, MODEL_WEIR_SETTING_PATH
from pyswmm.errors import OutputException

from swmm.toolkit.shared_enum import (
    LinkAttribute,
    NodeAttribute,
    SubcatchAttribute,
    SystemAttribute,
)
from datetime import datetime
from pathlib import Path
from swmm.toolkit import output as toolkit_output


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
        result = getattr(out, "{}_result".format(kind))(0, 0)
        raw_result = getattr(toolkit_output, "get_{}_result".format(kind))(
            out.handle, 0, 0
        )
        assert len(result) == len(raw_result)
        assert list(result.values()) == pytest.approx(raw_result)

        assert pickle.loads(pickle.dumps(result)) == result
        attributes = getattr(out, "{}_attributes".format(kind))
        first_pollutant = base_enum.POLLUT_CONC_0.value
        expected_names = [m.name for m in base_enum if m.value < first_pollutant]
        expected_names += ["POLLUT_CONC_{}".format(i) for i in range(count)]
        assert list(attributes) == expected_names
        assert [member.name for member in result] == expected_names
        assert list(result) == list(attributes.values())
        for name, member in original_members.items():
            if name in attributes:
                assert attributes[name] is member

        series = series_class(out)[0]
        for index in range(count):
            name = "POLLUT_CONC_{}".format(index)
            attribute = attributes[name]
            # Read complete raw rows so the reference does not rely on the
            # same attribute-enum conversion as the methods under test.
            raw_series = [
                getattr(toolkit_output, "get_{}_result".format(kind))(
                    out.handle, period, 0
                )[first_pollutant + index]
                for period in range(out.period)
            ]
            expected = dict(zip(out.times, raw_series))
            assert getattr(out, "{}_series".format(kind))(0, attribute) == expected
            assert getattr(series, name.lower()) == expected
            assert name.lower() in dir(series)
            # Exercise snapshots during a nonzero concentration, not just the
            # initially dry report where different pollutants can all be zero.
            report_index = max(range(out.period), key=raw_series.__getitem__)
            assert raw_series[report_index] > 0
            at_time = getattr(out, "{}_attribute".format(kind))(attribute, report_index)
            assert list(at_time.values())[0] == pytest.approx(raw_series[report_index])
        with pytest.raises(AttributeError):
            getattr(series, "pollut_conc_{}".format(count))
        assert "pollut_conc_{}".format(count) not in dir(series)
    assert base_enum.__members__ == original_members


def test_output_pollutant_attributes_are_isolated(pollutant_output_files):
    with (
        Output(pollutant_output_files[3]) as multiple,
        Output(pollutant_output_files[0]) as none,
        Output(pollutant_output_files[1]) as single,
    ):
        for kind in ("subcatch", "node", "link"):
            name = "{}_attributes".format(kind)
            multiple_attributes = getattr(multiple, name)
            assert "POLLUT_CONC_2" in multiple_attributes
            assert "POLLUT_CONC_0" not in getattr(none, name)
            assert "POLLUT_CONC_1" not in getattr(single, name)
            assert getattr(multiple, name) is multiple_attributes


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
