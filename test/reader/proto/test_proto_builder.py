import pytest

from monitor.reader.proto import (
    BasicInfoProtoBuilder,
    CPUProtoBuilder,
    MatrixInfoProtoBuilder,
    MemoryInfoProtoBuilder,
    NVGPUProtoBuilder,
    ProcessProtoBuilder,
    ProtoBuilder,
    TemperatureProtoBuilder,
)
from monitor.reader.proto.device_pb2 import (
    CPU,
    NVGPU,
    BasicInfo,
    MatrixInfo,
    MemoryInfo,
    Process,
    Temperature,
)


@pytest.mark.parametrize(
    "proto_builder, proto",
    [
        (TemperatureProtoBuilder, Temperature),
        (MemoryInfoProtoBuilder, MemoryInfo),
        (ProcessProtoBuilder, Process),
        (BasicInfoProtoBuilder, BasicInfo),
        (MatrixInfoProtoBuilder, MatrixInfo),
        (NVGPUProtoBuilder, NVGPU),
        (CPUProtoBuilder, CPU),
    ],
)
def test_proto(proto_builder: ProtoBuilder, proto):
    assert isinstance(proto_builder.build_proto(), proto)


def test_matrix_info_error():
    with pytest.raises(TypeError):
        MatrixInfoProtoBuilder.build_proto(usage="")
