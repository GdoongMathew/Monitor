from .device_monitor import NVGPUMonitor
from .device_monitor import CPUMonitor


class Device:
    device_id = None
    device_name = ''

    temperature = None
    memory_total = None
    memory_used = None
    memory_free = None
    memory_info = {}
    clock_speed = None

    _device_handle = None



