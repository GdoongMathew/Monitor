from monitor.reader.proto import TemperatureProtoBuilder
from monitor.reader.proto import MemoryInfoProtoBuilder
from monitor.reader.proto import ProcessProtoBuilder
from monitor.reader.proto import RepeatedProcessProtoBuilder
from monitor.reader.proto import BasicInfoProtoBuilder
from monitor.reader.proto import MatrixInfoProtoBuilder
from monitor.reader.proto import NVGPUProtoBuilder
from monitor.reader.proto import CPUProtoBuilder
from monitor.reader.proto import ProtoBuilder

from monitor.reader.proto.device_pb2 import *

from test_reader import gpu_reader
from test_reader import cpu_reader
import pytest


@pytest.mark.parametrize('proto_builder, proto', [
    (TemperatureProtoBuilder, Temperature),
    (MemoryInfoProtoBuilder, MemoryInfo),
    (ProcessProtoBuilder, Process),
    (BasicInfoProtoBuilder, BasicInfo),
    (MatrixInfoProtoBuilder, MatrixInfo),
    (NVGPUProtoBuilder, NVGPU),
    (CPUProtoBuilder, CPU),
])
def test_proto(proto_builder: ProtoBuilder, proto):
    assert isinstance(proto_builder.build_proto(), proto)


def test_matrix_info_error():
    with pytest.raises(TypeError):
        MatrixInfoProtoBuilder.build_proto(usage='')
