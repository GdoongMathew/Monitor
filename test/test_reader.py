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


@pytest.mark.parametrize('reader, basic_info, matrix_info',
                         [
                             ('cpu_reader', True, True),
                             ('cpu_reader', False, True),
                             ('cpu_reader', True, False),
                             ('gpu_reader', True, True),
                             ('gpu_reader', False, True),
                             ('gpu_reader', True, False),
                         ], indirect=['reader'])
def test_summary(reader, basic_info, matrix_info):
    summary = reader.summary(basic_info=basic_info, matrix_info=matrix_info)
    assert isinstance(summary, dict)

    if basic_info:
        assert set(reader._basic_info_list).issubset(summary.keys())
    else:
        assert not set(reader._basic_info_list).issubset(summary.keys())

    if matrix_info:
        assert set(reader._matrix_info_list).issubset(summary.keys())
    else:
        assert not set(reader._matrix_info_list).issubset(summary.keys())

