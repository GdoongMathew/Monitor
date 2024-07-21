import pytest

from monitor.reader import CPUReader, NVGPUReader


@pytest.fixture(scope="module")
def cpu_reader():
    return CPUReader()


@pytest.fixture(scope="module")
def gpu_reader():
    return NVGPUReader(idx=0)


@pytest.fixture(scope="module")
def non_reader():
    return None


@pytest.fixture(scope="module")
def reader(request):
    reader = request.getfixturevalue(request.param)
    return reader
