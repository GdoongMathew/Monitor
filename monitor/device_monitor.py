from . import *
from pynvml import *


class GPUMonitor(DeviceMonitor):
    def __init__(self, idx=None):
        nvmlInit()

        ids = list(range(nvmlDeviceGetCount()))
        if idx is not None:
            assert isinstance(idx, (int, str))
            idx = int(idx)
            assert idx in ids
            ids = [idx]
        
        self.gpu_handle = []
        for _id in ids:
            self.gpu_handle.append(nvmlDeviceGetIndex(_id))

    def summary(self): 
        pass

    def print(self):
        pass

    def temperature(self):
        for handle in self.gpu_handle:
            temp = nvmlDeviceGetTemperature(handle, 0)
        pass

    def total_mem_usage(self):
        pass


class CPUMonitor(DeviceMonitor):
    def __init__(self):
        pass

    def summary(self):
        pass

    def print(self):
        pass

    def temperature(self):
        pass

    def total_mem_usage(self):
        pass