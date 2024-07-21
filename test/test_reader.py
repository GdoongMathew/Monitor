from typing import TYPE_CHECKING

import pytest

from monitor.reader.proto.device_pb2 import CPU, NVGPU

if TYPE_CHECKING:
    from monitor.reader.device_reader import DeviceReader


@pytest.mark.parametrize("reader", ["cpu_reader", "gpu_reader"], indirect=["reader"])
def test_name(reader: "DeviceReader"):
    name = reader.name()
    if name is not None:
        assert isinstance(name, str)


@pytest.mark.parametrize(
    "reader, proto",
    [
        ("cpu_reader", CPU),
        ("gpu_reader", NVGPU),
    ],
    indirect=["reader"],
)
def test_proto(reader: "DeviceReader", proto):
    info = reader.to_proto(basic_info=True, matrix_info=False)
    assert isinstance(info, proto)


@pytest.mark.parametrize(
    "reader",
    ["cpu_reader", "gpu_reader"],
    indirect=["reader"],
)
@pytest.mark.parametrize(
    "basic_info",
    [True, False],
)
@pytest.mark.parametrize(
    "matrix_info",
    [True, False],
)
def test_summary(reader: "DeviceReader", basic_info, matrix_info):
    if not basic_info and not matrix_info:
        with pytest.raises(
            ValueError,
            match="Either one of basic_info or matrix_info should be True",
        ):
            reader.summary(basic_info=basic_info, matrix_info=matrix_info)
        return
    summary = reader.summary(basic_info=basic_info, matrix_info=matrix_info)
    assert isinstance(summary, dict)

    assert set(reader._basic_info_list).issubset(summary.keys()) == basic_info
    assert set(reader._matrix_info_list).issubset(summary.keys()) == matrix_info
