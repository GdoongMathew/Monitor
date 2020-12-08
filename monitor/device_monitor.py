from abc import abstractmethod
from monitor import *
from pynvml import *
import functools
import psutil


class DeviceMonitor:
    @abstractmethod
    def summary(self):
        # gathering information
        return NotImplementedError

    @abstractmethod
    def print(self):
        return NotImplementedError

    def temperature(self):
        return NotImplementedError

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

    @property
    def usage(self):
        return nvmlDeviceGetPerformanceState(self.gpu_handle)

    @property
    def temperature(self):
        return nvmlDeviceGetTemperature(self.gpu_handle, 0)

    @property
    def memory_info(self):
        return nvmlDeviceGetMemoryInfo(self.gpu_handle)


class CPUMonitor(DeviceMonitor):
    def __init__(self):
        pass

    def summary(self):
        pass

    def print(self):
        pass

    def temperature(self):
        pass

    def memory_info(self):
        p = psutil.Process(15)
        p.memory_percent()


if __name__ == '__main__':
    pass