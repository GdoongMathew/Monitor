import pytest

from monitor.reader import CPUReader


@pytest.fixture
def cpu_reader():
    return CPUReader()


def test_cpu_name(cpu_reader):
    assert isinstance(cpu_reader.name(), str)


def test_cpu_brand(cpu_reader):
    assert isinstance(cpu_reader.brand(), str)


def test_cpu_uuid(cpu_reader):
    assert isinstance(cpu_reader.uuid(), str)


def test_cpu_architecture(cpu_reader):
    assert isinstance(cpu_reader.architecture(), str)


@pytest.mark.parametrize(
    "fahrenheit",
    [True, False],
)
def test_cpu_temperature(cpu_reader, fahrenheit):
    temperature = cpu_reader.temperature(fahrenheit=fahrenheit)
    assert isinstance(temperature, dict)
    temp = temperature["Fahrenheit" if fahrenheit else "Celsius"]
    assert isinstance(temp, float)


def test_cpu_usage(cpu_reader):
    usage = cpu_reader.usage()
    assert isinstance(usage, dict)
    assert isinstance(usage["usage"], float)
    assert isinstance(usage["memory_usage"], float)
    assert 0.0 < usage["usage"] < 100.0
    assert 0.0 < usage["memory_usage"] < 100.0


def test_cpu_memory_info(cpu_reader):
    memory_info = cpu_reader.memory_info()
    assert isinstance(memory_info, dict)
    assert isinstance(memory_info["total"], int)
    assert isinstance(memory_info["free"], int)
    assert isinstance(memory_info["used"], int)


def test_cpu_process_info(cpu_reader):
    process_info = cpu_reader.process_info()
    assert isinstance(process_info, list)
    for process in process_info:
        assert isinstance(process, dict)
        assert "pid" in process
        assert "name" in process
        assert "usage" in process
        assert "used_memory" in process
