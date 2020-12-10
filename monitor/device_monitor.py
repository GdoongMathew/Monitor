from abc import abstractmethod
from pynvml import *
import platform
import os
import psutil
import subprocess
from .device_pb2 import *

if psutil.WINDOWS:
    import wmi

_nvml_initialized = False


def _nvml_init():
    global _nvml_initialized
    if not _nvml_initialized:
        nvmlInit()
        _nvml_initialized = True


def omit_nvml_error(nvml_error_codes):

    def wrapper(func):
        def inner(self, *args, **kwargs):
            try:
                ret = func(self, *args, **kwargs)
                return ret
            except NVMLError as e:
                if e.value in nvml_error_codes:
                    return None
                else:
                    raise e
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
    _summary_funcs = []

    def summary(self):
        # gathering information
        info = {}
        for func in self._summary_funcs:
            info[func] = self.__getattribute__(func)()
        return info

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

    _summary_funcs = ['index', 'name', 'uuid', 'serial', 'architecture', 'brand', 'driver_version',
                      'cuda_version', 'usage', 'power_usage', 'temperature', 'fan_speed',
                      'memory_info', 'process_info']

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

    def basic_proto(self):
        basic_info = BasicInfo()

        name = self.name()
        index = self.index()
        serial = self.serial()
        uuid = self.uuid()
        arch = self.architecture()
        brand = self.brand()

        basic_info.name = name if name is not None else ''
        basic_info.index = index if index is not None else -1
        basic_info.serial = serial if serial is not None else ''
        basic_info.uuid = uuid if uuid is not None else ''
        basic_info.architecture = arch if arch is not None else ''
        basic_info.brand = brand if brand is not None else ''

        return basic_info

    def matrix_info_proto(self):
        temp_proto = self.temperature()
        mem_proto = self.memory_info()
        usage = self.usage()
        info_proto = CommonMatrixInfo()
        info_proto.temperature.CopyFrom(temp_proto)
        info_proto.memory_info.CopyFrom(mem_proto)
        info_proto.usage = usage.gpu
        info_proto.memory_usage = usage.memory
        return info_proto

    def gpu_proto(self):
        nv_gpu = NVGPU()
        info = self.basic_proto()
        matrix = self.matrix_info_proto()
        processes = self.process_info()
        nv_gpu.info.CopyFrom(info)
        nv_gpu.matrix.CopyFrom(matrix)
        for p in processes.values():
            _proc = nv_gpu.process.add()
            _proc.CopyFrom(p)

        cuda_ver = self.cuda_version()
        cuda_cap = self.cuda_capacity()
        driver_ver = self.driver_version()
        nv_gpu.cuda_version = cuda_ver if cuda_ver is not None else -1
        nv_gpu.cuda_capacity = cuda_cap if cuda_cap is not None else ''
        nv_gpu.driver_version = driver_ver if driver_ver is not None else ''
        return nv_gpu


    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND])
    def name(self):
        return nvmlDeviceGetName(self.gpu_handle).decode('utf-8')

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND])
    def index(self):
        return nvmlDeviceGetIndex(self.gpu_handle)

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND])
    def uuid(self):
        return nvmlDeviceGetUUID(self.gpu_handle)

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND, NVML_ERROR_NOT_SUPPORTED])
    def serial(self):
        return nvmlDeviceGetSerial(self.gpu_handle)

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND, NVML_ERROR_NOT_SUPPORTED])
    def architecture(self):
        return self._NVML_ARCH[nvmlDeviceGetArchitecture(self.gpu_handle)]

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND, NVML_ERROR_NOT_SUPPORTED])
    def brand(self):
        return self._NVML_BRAND[nvmlDeviceGetBrand(self.gpu_handle)]

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND, NVML_ERROR_NOT_SUPPORTED])
    def driver_version(self):
        return nvmlSystemGetDriverVersion().decode('utf-8')

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND])
    def cuda_version(self):
        return nvmlSystemGetCudaDriverVersion_v2()

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND])
    def cuda_capacity(self):
        return str(nvmlDeviceGetCudaComputeCapability(self.gpu_handle))

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND])
    def usage(self):
        return nvmlDeviceGetUtilizationRates(self.gpu_handle)

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND])
    def power_usage(self):
        return nvmlDeviceGetPowerUsage(self.gpu_handle)

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND])
    def temperature(self, fahrenheit=False):
        temp = Temperature()
        _temp = nvmlDeviceGetTemperature(self.gpu_handle, NVML_TEMPERATURE_GPU)
        if fahrenheit:
            temp.Fahrenheit = (float(_temp) * 9 / 5) + 32
        else:
            temp.Celsius = _temp
        return temp

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND, NVML_ERROR_NOT_SUPPORTED])
    def fan_speed(self):
        return nvmlDeviceGetFanSpeed(self.gpu_handle)

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND, NVML_ERROR_NOT_SUPPORTED])
    def memory_info(self):
        mem_info = MemoryInfo()
        val = nvmlDeviceGetMemoryInfo(self.gpu_handle)
        mem_info.total = val.total
        mem_info.free = val.free
        mem_info.used = val.used
        return mem_info

    @omit_nvml_error([NVML_ERROR_FUNCTION_NOT_FOUND])
    def process_info(self):
        _procs = nvmlDeviceGetComputeRunningProcesses(self.gpu_handle)
        _procs.extend(nvmlDeviceGetGraphicsRunningProcesses(self.gpu_handle))
        ret = {}

        for _p in _procs:
            if _p.pid in ret:
                continue
            try:
                proc_name = str(nvmlSystemGetProcessName(_p.pid), encoding='big5').split('\\')[-1]
            except nvmlExceptionClass(NVML_ERROR_NO_PERMISSION):
                proc_name = psutil.Process(pid=_p.pid).name()

            proc = Process()
            proc.pid = _p.pid
            proc.name = proc_name
            proc.memory = _p.usedGpuMemory if _p.usedGpuMemory is not None else -1
            proc.usage = -1 # if in the future we can get gpu usage per process
            ret[_p.pid] = proc
        return ret


class CPUMonitor(DeviceMonitor):
    _summary_funcs = ['name', 'uuid', 'architecture', 'brand', 'temperature', 'usage', 'memory_info']

    def __init__(self):
        pass

    def name(self):
        name = subprocess.check_output(["wmic", "cpu", "get", "name"]).decode('utf-8').strip().split("\n")[1]
        return name

    def brand(self):
        return platform.processor()

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
                           'used_memory': _p.info['memory_info'].vms}
        return ret


if __name__ == '__main__':
    pass