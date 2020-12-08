from abc import abstractmethod
from monitor import *
from pynvml import *
import platform
import psutil


def omit_nvml_error(nvml_error_code):
    def wrapper(func):
        def inner(self, *args, **kwargs):
            try:
                ret = func(self, *args, **kwargs)
                return ret
            except NVMLError(nvml_error_code):
                return None

        return inner
    return wrapper


def bytes_converter(_b, unit='mb'):
    _unit_map = {
        'b': pow(1024, 0),
        'kb': pow(1024, 1),
        'mb': pow(1024, 2),
        'gb': pow(1024, 3),
        'tb': pow(1024, 4)
    }
    assert unit in _unit_map, f'{unit} is not supported.'
    return _b / _unit_map[unit]


def nvml_struct_to_dict(_structure):
    return {i: getattr(_structure, i) for i, _ in _structure._fields_}


class DeviceMonitor:
    @abstractmethod
    def summary(self):
        # gathering information
        return NotImplementedError

    @abstractmethod
    def print(self):
        return NotImplementedError

    @abstractmethod
    def temperature(self):
        return NotImplementedError

    @abstractmethod
    def memory_info(self):
        return NotImplementedError


class NVGPUMonitor(DeviceMonitor):
    nvmlInit()

    def __init__(self, idx=None, uuid=None, pci_bus_id=None, serial=None):
        _kwargs = [idx, uuid, pci_bus_id, serial]
        assert _kwargs.count(None) >= 3, 'provide not more than one of idx, uuid, pci_bus_id or serial.'
        if _kwargs.count(None) == 4:
            idx = 0

        _create_handle_func = {
            'idx': nvmlDeviceGetHandleByIndex,
            'uuid': nvmlDeviceGetHandleByUUID,
            'pci_bus_id': nvmlDeviceGetHandleByPciBusId,
            'serial': nvmlDeviceGetHandleBySerial
        }

        if idx is not None:
            assert isinstance(idx, int)
            _handle_func = _create_handle_func['idx']
            _func_input = idx

        elif uuid is not None:
            assert isinstance(uuid, str)
            _handle_func = _create_handle_func['uuid']
            _func_input = bytes(uuid, encoding='utf-8')

        elif pci_bus_id is not None:
            assert isinstance(pci_bus_id, str)
            _handle_func = _create_handle_func['pci_bus_id']
            _func_input = bytes(pci_bus_id, encoding='utf-8')

        else:
            # serial
            assert isinstance(serial, str)
            _handle_func = _create_handle_func['serial']
            _func_input = bytes(serial, encoding='utf-8')

        self.gpu_handle = _handle_func(_func_input)

    def summary(self): 
        pass

    def print(self):
        pass

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def name(self):
        return nvmlDeviceGetName(self.gpu_handle).decode('utf-8')

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def architecture(self):
        return nvmlDeviceGetArchitecture(self.gpu_handle.contents)

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def usage(self):
        return nvml_struct_to_dict(nvmlDeviceGetUtilizationRates(self.gpu_handle))

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def temperature(self, fahrenheit=False):
        _temp = nvmlDeviceGetTemperature(self.gpu_handle, NVML_TEMPERATURE_GPU)
        return (float(_temp) * 9 / 5) + 32 if fahrenheit else _temp

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def fans_speed(self):
        return nvmlDeviceGetFanSpeed(self.gpu_handle)

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def memory_info(self):
        return nvml_struct_to_dict(nvmlDeviceGetMemoryInfo(self.gpu_handle))

    def process_info(self):
        _procs = nvmlDeviceGetComputeRunningProcesses(self.gpu_handle)
        ret = {}
        for _p in _procs:
            try:
                proc_name = str(nvmlSystemGetProcessName(_procs), encoding='big5').split('\\')[-1]
            except NVMLError(NVML_ERROR_NO_PERMISSION):
                proc_name = psutil.Process(pid=_p.pid).name()

            ret[_p.pid] = {'name': proc_name,
                           'used_memory': _p.usedGpuMemory}
        return ret


class CPUMonitor(DeviceMonitor):
    def __init__(self):
        pass

    def summary(self):
        pass

    def print(self):
        pass

    def architecture(self):
        return platform.machine()

    def temperature(self, fahrenheit=False):
        if psutil.LINUX or psutil.MACOS:
            return psutil.sensors_temperatures(fahrenheit=fahrenheit)

        pass

    def memory_info(self):
        v_mem = psutil.virtual_memory()
        return {'total': v_mem.total,
                'free': v_mem.available,
                'used': v_mem.total - v_mem.available}


if __name__ == '__main__':
    pass