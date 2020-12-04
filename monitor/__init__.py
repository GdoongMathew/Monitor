from abc import abstractmethod
import psutil


class Device:
    temperature = None
    memory_total = None
    memory_used = None
    memory_free = None
    memory_info = {}
    clock_speed = None


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

    def total_mem_usage(self):
        return NotImplementedError
