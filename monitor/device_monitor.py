from abc import abstractmethod
from pynvml import *
import platform
import os
import psutil

if psutil.WINDOWS:
    import wmi

_nvml_initialized = False


def _nvml_init():
    global _nvml_initialized
    if not _nvml_initialized:
        nvmlInit()
        _nvml_initialized = True


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
    def temperature(self):
        return NotImplementedError

    @abstractmethod
    def memory_info(self):
        return NotImplementedError


class NVGPUMonitor(DeviceMonitor):
    _nvml_init()

    _NVML_ARCH = {
        NVML_DEVICE_ARCH_UNKNOWN: 'UNK',
        NVML_DEVICE_ARCH_KEPLER: 'Kepler',
        NVML_DEVICE_ARCH_MAXWELL: 'Maxwell',
        NVML_DEVICE_ARCH_PASCAL: 'Pascal',
        NVML_DEVICE_ARCH_VOLTA: 'Volta',
        NVML_DEVICE_ARCH_TURING: 'Turing',
        NVML_DEVICE_ARCH_AMPERE: 'Ampere',
    }

    _NVML_BRAND = {
        NVML_BRAND_UNKNOWN: 'UNK',
        NVML_BRAND_QUADRO: 'Quadro',
        NVML_BRAND_TESLA: 'Tesla',
        NVML_BRAND_NVS: 'Nvs',
        NVML_BRAND_GRID: 'Grid',
        NVML_BRAND_GEFORCE: 'GeForce',
        NVML_BRAND_TITAN: 'Titan',
        NVML_BRAND_COUNT: 'Count',
    }

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

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def name(self):
        return nvmlDeviceGetName(self.gpu_handle).decode('utf-8')

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def index(self):
        return nvmlDeviceGetIndex(self.gpu_handle)

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def uuid(self):
        return nvmlDeviceGetUUID(self.gpu_handle)

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def architecture(self):
        return nvmlDeviceGetArchitecture(self.gpu_handle.contents)

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def driver_version(self):
        return nvmlSystemGetDriverVersion().decode('utf-8')

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def cuda_version(self):
        return nvmlSystemGetCudaDriverVersion_v2()

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def cuda_capacity(self):
        return str(nvmlDeviceGetCudaComputeCapability(self.gpu_handle))

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def usage(self):
        return nvml_struct_to_dict(nvmlDeviceGetUtilizationRates(self.gpu_handle))

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def power_usage(self):
        return nvmlDeviceGetPowerUsage(self.gpu_handle)

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

    @omit_nvml_error(NVML_ERROR_FUNCTION_NOT_FOUND)
    def process_info(self):
        _procs = nvmlDeviceGetComputeRunningProcesses(self.gpu_handle)
        _procs.extend(nvmlDeviceGetGraphicsRunningProcesses(self.gpu_handle))
        ret = {}
        for _p in _procs:
            if _p.pid in ret:
                continue
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

    def uuid(self):
        if psutil.LINUX:
            return os.popen("hdparm -I /dev/sda | grep 'Serial Number'").read().split()[-1]
        elif psutil.WINDOWS:
            return wmi.WMI().Win32_ComputerSystemProduct()[0].UUID
        else:
            return None

    def architecture(self):
        return platform.machine()

    def temperature(self, fahrenheit=False):
        if psutil.LINUX or psutil.MACOS:
            temp_readings = psutil.sensors_temperatures(fahrenheit=fahrenheit)['coretemp']
            temp = []
            for reading in temp_readings:
                if 'Core' in reading.label:
                    temp.append(reading.current)

            return sum(temp) / len(temp) if temp else None

        else:
            return None

    def usage(self):
        mem_info = self.memory_info()
        return {'cpu': psutil.cpu_percent(0.05),
                'memory': mem_info['used'] / mem_info['total'] * 100}

    def memory_info(self):
        v_mem = psutil.virtual_memory()
        return {'total': v_mem.total,
                'free': v_mem.available,
                'used': v_mem.total - v_mem.available}

    def process_info(self):
        ret = {}
        for _p in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
            ret[_p.pid] = {'name': _p.info['name'],
                           'usage': _p.info['cpu_percent'],
                           'used_memory': _p.info['cpu_percent'].vms}
        return ret


if __name__ == '__main__':
    pass