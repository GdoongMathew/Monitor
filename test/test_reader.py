from monitor import CPUReader, NVGPUReader
from monitor.reader.proto.device_pb2 import NVGPU
from monitor.reader.proto.device_pb2 import CPU
import pytest


@pytest.fixture
def cpu_reader():
    return CPUReader()


@pytest.fixture
def gpu_reader():
    return NVGPUReader(idx=0)


@pytest.fixture
def reader(request):
    reader = request.getfixturevalue(request.param)
    return reader


@pytest.mark.parametrize("reader",
                         [
                             'cpu_reader',
                             'gpu_reader'
                         ], indirect=['reader'])
def test_name(reader):
    name = reader.name()
    if name is not None:
        assert isinstance(name, str)


@pytest.mark.parametrize("reader, proto",
                         [
                             ('cpu_reader', CPU),
                             ('gpu_reader', NVGPU)
                         ], indirect=['reader'])
def test_proto(reader, proto):
    info = reader.to_proto()
    assert isinstance(info, proto)

