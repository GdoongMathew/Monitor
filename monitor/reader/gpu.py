from __future__ import annotations

from functools import lru_cache
from typing import Callable, Optional

import psutil
import pynvml

from monitor.reader.base import DeviceReader
from monitor.reader.proto import NVGPUProtoBuilder


def omit_nvml_error(nvml_error_codes):
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                ret = func(*args, **kwargs)
                return ret
            except pynvml.NVMLError as e:
                if e.value in nvml_error_codes:
                    return None
                else:
                    raise e

        return inner

    return wrapper


def nvml_init(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        pynvml.nvmlInit()
        return func(*args, **kwargs)

    return wrapper


class NVGPUReader(DeviceReader):
    _NVML_ARCH = {
        pynvml.NVML_DEVICE_ARCH_UNKNOWN: "UNK",
        pynvml.NVML_DEVICE_ARCH_KEPLER: "Kepler",
        pynvml.NVML_DEVICE_ARCH_MAXWELL: "Maxwell",
        pynvml.NVML_DEVICE_ARCH_PASCAL: "Pascal",
        pynvml.NVML_DEVICE_ARCH_VOLTA: "Volta",
        pynvml.NVML_DEVICE_ARCH_TURING: "Turing",
        pynvml.NVML_DEVICE_ARCH_AMPERE: "Ampere",
        pynvml.NVML_DEVICE_ARCH_ADA: "Ada",
        pynvml.NVML_DEVICE_ARCH_HOPPER: "Hopper",
    }

    _NVML_BRAND = {
        pynvml.NVML_BRAND_UNKNOWN: "UNK",
        pynvml.NVML_BRAND_QUADRO: "Quadro",
        pynvml.NVML_BRAND_TESLA: "Tesla",
        pynvml.NVML_BRAND_NVS: "NVS",
        pynvml.NVML_BRAND_GRID: "Grid",
        pynvml.NVML_BRAND_GEFORCE: "GeForce",
        pynvml.NVML_BRAND_TITAN: "Titan",
        pynvml.NVML_BRAND_NVIDIA_VAPPS: "NVIDIA Virtual Application",
        pynvml.NVML_BRAND_NVIDIA_VPC: "NVIDIA Virtual PC",
        pynvml.NVML_BRAND_NVIDIA_VCS: "NVIDIA Virtual Computer Server",
        pynvml.NVML_BRAND_NVIDIA_VWS: "NVIDIA RTX Virtual Workstation",
        pynvml.NVML_BRAND_NVIDIA_CLOUD_GAMING: "NVIDIA Cloud Gaming",
        # NVML_BRAND_NVIDIA_VGAMING: 'NVIDIA vGaming',
        pynvml.NVML_BRAND_QUADRO_RTX: "Quadro RTX",
        pynvml.NVML_BRAND_NVIDIA_RTX: "Nvidia RTX",
        pynvml.NVML_BRAND_NVIDIA: "NVIDIA",
        pynvml.NVML_BRAND_GEFORCE_RTX: "GeForce RTX",
        pynvml.NVML_BRAND_TITAN_RTX: "Titan RTX",
    }

    _basic_info_list = [
        "index",
        "name",
        "uuid",
        "serial",
        "architecture",
        "brand",
    ]
    _matrix_info_list = [
        "driver_version",
        "cuda_version",
        "usage",
        "power_usage",
        "temperature",
        "fan_speed",
        "memory_info",
        "process_info",
    ]

    def __init__(
        self,
        *,
        idx: Optional[int] = None,
        uuid: Optional[str] = None,
        pci_bus_id: Optional[str] = None,
        serial: Optional[str] = None,
    ):
        _kwargs = [idx, uuid, pci_bus_id, serial]
        if _kwargs.count(None) < 3:
            raise ValueError("provide not more than one of idx, uuid, pci_bus_id or serial.")
        if _kwargs.count(None) == 4:
            idx = 0

        if idx is not None:
            if not isinstance(idx, int):
                raise TypeError(f"idx should be an integer, get {type(idx)}.")
            _handle_func = pynvml.nvmlDeviceGetHandleByIndex
            _func_input = idx

        elif uuid is not None:
            if not isinstance(uuid, str):
                raise TypeError(f"uuid should be a str, get {type(uuid)}.")
            _handle_func = pynvml.nvmlDeviceGetHandleByUUID
            _func_input = bytes(uuid, encoding="utf-8")

        elif pci_bus_id is not None:
            if not isinstance(pci_bus_id, str):
                raise TypeError(f"pci_bus_id should be a str, get {type(pci_bus_id)}.")
            _handle_func = pynvml.nvmlDeviceGetHandleByPciBusId
            _func_input = bytes(pci_bus_id, encoding="utf-8")

        else:
            # serial
            if not isinstance(serial, str):
                raise TypeError(f"serial should be a str, get {type(serial)}.")
            _handle_func = pynvml.nvmlDeviceGetHandleBySerial
            _func_input = bytes(serial, encoding="utf-8")

        self.gpu_handle = nvml_init(_handle_func)(_func_input)

    def to_proto(
        self,
        basic_info: bool = True,
        matrix_info: bool = True,
    ) -> NVGPUProtoBuilder:
        ret = self.summary(basic_info=basic_info, matrix_info=matrix_info)
        return NVGPUProtoBuilder.build_proto(**ret)

    @lru_cache
    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def name(self) -> str:
        return pynvml.nvmlDeviceGetName(self.gpu_handle)

    @lru_cache
    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def index(self) -> int:
        return pynvml.nvmlDeviceGetIndex(self.gpu_handle)

    @lru_cache
    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def uuid(self) -> str:
        return pynvml.nvmlDeviceGetUUID(self.gpu_handle)

    @lru_cache
    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_NOT_SUPPORTED,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def serial(self):
        return pynvml.nvmlDeviceGetSerial(self.gpu_handle)

    @lru_cache
    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_NOT_SUPPORTED,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def architecture(self) -> str:
        return self._NVML_ARCH[pynvml.nvmlDeviceGetArchitecture(self.gpu_handle)]

    @lru_cache
    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_NOT_SUPPORTED,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def brand(self) -> str:
        return self._NVML_BRAND[pynvml.nvmlDeviceGetBrand(self.gpu_handle)]

    @nvml_init
    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND, pynvml.NVML_ERROR_NOT_SUPPORTED, pynvml.NVML_ERROR_UNKNOWN])
    def driver_version(self) -> str:
        return pynvml.nvmlSystemGetDriverVersion()

    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def cuda_version(self) -> int:
        return pynvml.nvmlSystemGetCudaDriverVersion_v2()

    @lru_cache
    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def cuda_capacity(self) -> str:
        return str(pynvml.nvmlDeviceGetCudaComputeCapability(self.gpu_handle))

    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def usage(self) -> dict[str, int]:
        usage = pynvml.nvmlDeviceGetUtilizationRates(self.gpu_handle)
        return {"usage": usage.gpu, "memory_usage": usage.memory}

    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def power_usage(self) -> int:
        return pynvml.nvmlDeviceGetPowerUsage(self.gpu_handle)

    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def temperature(self, fahrenheit=False) -> dict[str, float]:
        _temp = pynvml.nvmlDeviceGetTemperature(self.gpu_handle, pynvml.NVML_TEMPERATURE_GPU)
        return {"Fahrenheit": (float(_temp) * 9 / 5) + 32} if fahrenheit else {"Celsius": _temp}

    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_NOT_SUPPORTED,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def fan_speed(self):
        return pynvml.nvmlDeviceGetFanSpeed(self.gpu_handle)

    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_NOT_SUPPORTED,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def memory_info(self) -> dict[str, int]:
        val = pynvml.nvmlDeviceGetMemoryInfo(self.gpu_handle)
        ret = {"total": val.total, "free": val.free, "used": val.used}
        return ret

    @nvml_init
    @omit_nvml_error(
        [
            pynvml.NVML_ERROR_FUNCTION_NOT_FOUND,
            pynvml.NVML_ERROR_UNKNOWN,
        ]
    )
    def process_info(self) -> list[dict[str, int]]:
        _procs = pynvml.nvmlDeviceGetComputeRunningProcesses(self.gpu_handle)
        _procs.extend(pynvml.nvmlDeviceGetGraphicsRunningProcesses(self.gpu_handle))
        ret = []

        for _p in _procs:
            if _p.pid in ret:
                continue
            try:
                proc_name = pynvml.nvmlSystemGetProcessName(_p.pid).split("\\")[-1]
            except pynvml.nvmlExceptionClass(pynvml.NVML_ERROR_NO_PERMISSION):
                proc_name = psutil.Process(pid=_p.pid).name()

            ret.append(
                {
                    "pid": _p.pid,
                    "name": proc_name,
                    "memory": _p.usedGpuMemory,
                }
            )
        return ret
