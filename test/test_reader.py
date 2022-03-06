from reader import CPUReader, NVGPUReader
from reader.proto.device_pb2 import NVGPU
from reader.proto.device_pb2 import CPU
import pytest


@pytest.fixture
def cpu_reader():
    return CPUReader()


@pytest.fixture
def gpu_reader():
    return NVGPUReader(idx=0)


def test_nvgpu_reader(gpu_reader):
    info = gpu_reader.to_proto()
    assert isinstance(info, NVGPU)


def test_cpu_reader(cpu_reader):
    info = cpu_reader.to_proto()
    assert isinstance(info, CPU)


