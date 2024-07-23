from unittest import mock

import pynvml
import pytest

from monitor.reader.gpu import NVGPUReader, nvml_init


def test_mvml_init():
    with mock.patch("pynvml.nvmlInit") as mock_nvml_init:
        nvml_init(lambda x: x)(None)
        mock_nvml_init.assert_called_once()


@pytest.fixture
def gpu_reader(scope="session"):
    return NVGPUReader()


@pytest.fixture(scope="session")
def nvml_handle():
    pynvml.nvmlInit()
    return pynvml.nvmlDeviceGetHandleByIndex(0)


def test_gpu_reader_init_not_valid():
    with pytest.raises(ValueError, match="provide not more than one of idx, uuid, pci_bus_id or serial."):
        NVGPUReader(idx=0, uuid="")


@pytest.mark.parametrize("idx", ["0", {}, [], 0.1])
def test_gpu_reader_init_idx_type(idx):
    with pytest.raises(TypeError, match=f"idx should be an integer, get {type(idx)}."):
        NVGPUReader(idx=idx)


def test_gpu_reader_init_idx(nvml_handle):
    idx = pynvml.nvmlDeviceGetIndex(nvml_handle)
    NVGPUReader(idx=idx)


def test_gpu_reader_init_uuid(nvml_handle):
    uuid = pynvml.nvmlDeviceGetUUID(nvml_handle)
    NVGPUReader(uuid=uuid)


def test_gpu_reader_init_pci_bus_id(nvml_handle):
    pci_bus_id = pynvml.nvmlDeviceGetPciInfo(nvml_handle).busId
    NVGPUReader(pci_bus_id=pci_bus_id)


def test_gpu_reader_init_serial(nvml_handle):
    serial = pynvml.nvmlDeviceGetSerial(nvml_handle)
    NVGPUReader(serial=serial)


def test_gpu_reader_name(gpu_reader, nvml_handle):
    name = pynvml.nvmlDeviceGetName(nvml_handle)
    reader_name = gpu_reader.name()
    assert reader_name == name
    assert isinstance(reader_name, str)


def test_gpu_reader_index(gpu_reader, nvml_handle):
    index = pynvml.nvmlDeviceGetIndex(nvml_handle)
    reader_index = gpu_reader.index()
    assert reader_index == index
    assert isinstance(reader_index, int)


def test_gpu_reader_uuid(gpu_reader, nvml_handle):
    uuid = pynvml.nvmlDeviceGetUUID(nvml_handle)
    reader_uuid = gpu_reader.uuid()
    assert reader_uuid == uuid
    assert isinstance(reader_uuid, str)


def test_gpu_reader_serial(gpu_reader, nvml_handle):
    serial = pynvml.nvmlDeviceGetSerial(nvml_handle)
    reader_serial = gpu_reader.serial()
    assert reader_serial == serial
    assert isinstance(reader_serial, str)


def test_gpu_reader_architecture(gpu_reader, nvml_handle):
    architecture = pynvml.nvmlDeviceGetArchitecture(nvml_handle)
    reader_architecture = gpu_reader.architecture()
    assert reader_architecture == gpu_reader._NVML_ARCH[architecture]
    assert isinstance(reader_architecture, str)


def test_gpu_reader_brand(gpu_reader, nvml_handle):
    brand = pynvml.nvmlDeviceGetBrand(nvml_handle)
    reader_brand = gpu_reader.brand()
    assert reader_brand == gpu_reader._NVML_BRAND[brand]
    assert isinstance(reader_brand, str)


def test_gpu_reader_driver_version(gpu_reader, nvml_handle):
    driver_version = pynvml.nvmlSystemGetDriverVersion()
    reader_driver = gpu_reader.driver_version()
    assert reader_driver == driver_version
    assert isinstance(reader_driver, str)


def test_gpu_reader_cuda_version(gpu_reader, nvml_handle):
    cuda_version = pynvml.nvmlSystemGetCudaDriverVersion()
    reader_cuda = gpu_reader.cuda_version()
    assert reader_cuda == cuda_version
    assert isinstance(reader_cuda, int)


def test_gpu_reader_cuda_capacity(gpu_reader, nvml_handle):
    cuda_capacity = str(pynvml.nvmlDeviceGetCudaComputeCapability(nvml_handle))
    reader_cuda_capacity = gpu_reader.cuda_capacity()
    assert reader_cuda_capacity == cuda_capacity
    assert isinstance(reader_cuda_capacity, str)


def test_gpu_reader_usage(gpu_reader, nvml_handle):
    usage = pynvml.nvmlDeviceGetUtilizationRates(nvml_handle)
    reader_usage = gpu_reader.usage()
    assert isinstance(reader_usage, dict)
    assert isinstance(reader_usage["usage"], int)
    assert reader_usage["usage"] == usage.gpu
    assert "memory_usage" in reader_usage
    assert isinstance(reader_usage["memory_usage"], int)
    assert reader_usage["memory_usage"] == usage.memory


def test_gpu_reader_power_usage(gpu_reader, nvml_handle):
    power_usage = pynvml.nvmlDeviceGetPowerUsage(nvml_handle)
    reader_power_usage = gpu_reader.power_usage()
    assert reader_power_usage == power_usage
    assert isinstance(reader_power_usage, int)


@pytest.mark.parametrize("fahrenheit", [True, False])
def test_gpu_reader_temperature(gpu_reader, nvml_handle, fahrenheit):
    temperature = pynvml.nvmlDeviceGetTemperature(nvml_handle, pynvml.NVML_TEMPERATURE_GPU)
    reader_temp = gpu_reader.temperature(fahrenheit=fahrenheit)
    if fahrenheit:
        assert reader_temp["Fahrenheit"] == temperature * 9 / 5 + 32
    else:
        assert reader_temp["Celsius"] == temperature
