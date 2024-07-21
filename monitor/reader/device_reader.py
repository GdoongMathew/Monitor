from __future__ import annotations

import os
import platform
import subprocess
from abc import abstractmethod

import psutil
import pynvml

from .proto import CPUProtoBuilder, NVGPUProtoBuilder

if psutil.WINDOWS:
    import pythoncom
    import wmi

    pythoncom.CoInitialize()


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


def bytes_converter(_b, unit="mb"):
    _unit_map = {
        "b": pow(1024, 0),
        "kb": pow(1024, 1),
        "mb": pow(1024, 2),
        "gb": pow(1024, 3),
        "tb": pow(1024, 4),
    }
    assert unit in _unit_map, f"{unit} is not supported."
    return _b / _unit_map[unit]


def nvml_struct_to_dict(_structure):
    return {i: getattr(_structure, i) for i, _ in _structure._fields_}


class DeviceReader:
    _basic_info_list = []
    _matrix_info_list = []

    def summary(self, basic_info=True, matrix_info=True):
        # gathering information
        info = {}
        _info_list = []
        if not basic_info and not matrix_info:
            raise ValueError("Either one of basic_info or matrix_info should be True")
        if basic_info:
            _info_list.extend(self._basic_info_list)
        if matrix_info:
            _info_list.extend(self._matrix_info_list)
        for func in _info_list:
            info[func] = self.__getattribute__(func)()
        return info

    def name(self) -> str:
        return "Unknown Device"

    @abstractmethod
    def temperature(self):
        raise NotImplementedError

    @abstractmethod
    def memory_info(self):
        raise NotImplementedError

    @abstractmethod
    def to_proto(self, **kwargs):
        raise NotImplementedError


class NVGPUReader(DeviceReader):
    pynvml.nvmlInit()

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

    _basic_info_list = ["index", "name", "uuid", "serial", "architecture", "brand"]
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

    def __init__(self, idx=None, uuid=None, pci_bus_id=None, serial=None):
        _kwargs = [idx, uuid, pci_bus_id, serial]
        if _kwargs.count(None) < 3:
            raise ValueError("provide not more than one of idx, uuid, pci_bus_id or serial.")
        if _kwargs.count(None) == 4:
            idx = 0

        _create_handle_func = {
            "idx": pynvml.nvmlDeviceGetHandleByIndex,
            "uuid": pynvml.nvmlDeviceGetHandleByUUID,
            "pci_bus_id": pynvml.nvmlDeviceGetHandleByPciBusId,
            "serial": pynvml.nvmlDeviceGetHandleBySerial,
        }

        if idx is not None:
            if not isinstance(idx, int):
                raise TypeError(f"idx should be integer, get {type(idx)}.")
            _handle_func = _create_handle_func["idx"]
            _func_input = idx

        elif uuid is not None:
            if not isinstance(uuid, str):
                raise TypeError(f"uuid should be integer, get {type(uuid)}.")
            _handle_func = _create_handle_func["uuid"]
            _func_input = bytes(uuid, encoding="utf-8")

        elif pci_bus_id is not None:
            if not isinstance(pci_bus_id, str):
                raise TypeError(f"pci_bus_id should be integer, get {type(pci_bus_id)}.")
            _handle_func = _create_handle_func["pci_bus_id"]
            _func_input = bytes(pci_bus_id, encoding="utf-8")

        else:
            # serial
            if not isinstance(serial, str):
                raise TypeError(f"serial should be integer, get {type(serial)}.")
            _handle_func = _create_handle_func["serial"]
            _func_input = bytes(serial, encoding="utf-8")

        self.gpu_handle = _handle_func(_func_input)

    def to_proto(self, basic_info=True, matrix_info=True):
        ret = self.summary(basic_info=basic_info, matrix_info=matrix_info)
        return NVGPUProtoBuilder.build_proto(**ret)

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND])
    def name(self) -> str:
        return pynvml.nvmlDeviceGetName(self.gpu_handle)

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND])
    def index(self) -> int:
        return pynvml.nvmlDeviceGetIndex(self.gpu_handle)

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND])
    def uuid(self):
        return pynvml.nvmlDeviceGetUUID(self.gpu_handle)

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND, pynvml.NVML_ERROR_NOT_SUPPORTED])
    def serial(self):
        return pynvml.nvmlDeviceGetSerial(self.gpu_handle)

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND, pynvml.NVML_ERROR_NOT_SUPPORTED])
    def architecture(self):
        return self._NVML_ARCH[pynvml.nvmlDeviceGetArchitecture(self.gpu_handle)]

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND, pynvml.NVML_ERROR_NOT_SUPPORTED])
    def brand(self):
        return self._NVML_BRAND[pynvml.nvmlDeviceGetBrand(self.gpu_handle)]

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND, pynvml.NVML_ERROR_NOT_SUPPORTED])
    def driver_version(self) -> str:
        return pynvml.nvmlSystemGetDriverVersion()

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND])
    def cuda_version(self):
        return pynvml.nvmlSystemGetCudaDriverVersion_v2()

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND])
    def cuda_capacity(self):
        return str(pynvml.nvmlDeviceGetCudaComputeCapability(self.gpu_handle))

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND])
    def usage(self):
        usage = pynvml.nvmlDeviceGetUtilizationRates(self.gpu_handle)
        return {"usage": usage.gpu, "memory_usage": usage.memory}

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND])
    def power_usage(self):
        return pynvml.nvmlDeviceGetPowerUsage(self.gpu_handle)

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND])
    def temperature(self, fahrenheit=False):
        _temp = pynvml.nvmlDeviceGetTemperature(self.gpu_handle, pynvml.NVML_TEMPERATURE_GPU)
        return {"Fahrenheit": (float(_temp) * 9 / 5) + 32} if fahrenheit else {"Celsius": _temp}

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND, pynvml.NVML_ERROR_NOT_SUPPORTED])
    def fan_speed(self):
        return pynvml.nvmlDeviceGetFanSpeed(self.gpu_handle)

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND, pynvml.NVML_ERROR_NOT_SUPPORTED])
    def memory_info(self):
        val = pynvml.nvmlDeviceGetMemoryInfo(self.gpu_handle)
        ret = {"total": val.total, "free": val.free, "used": val.used}
        return ret

    @omit_nvml_error([pynvml.NVML_ERROR_FUNCTION_NOT_FOUND])
    def process_info(self):
        _procs = pynvml.nvmlDeviceGetComputeRunningProcesses(self.gpu_handle)
        _procs.extend(pynvml.nvmlDeviceGetGraphicsRunningProcesses(self.gpu_handle))
        ret = []

        for _p in _procs:
            if _p.pid in ret:
                continue
            try:
                proc_name = str(pynvml.nvmlSystemGetProcessName(_p.pid), encoding="big5").split("\\")[-1]
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


class CPUReader(DeviceReader):
    _basic_info_list = ["name", "uuid", "architecture", "brand"]
    _matrix_info_list = ["temperature", "usage", "memory_info"]

    def __init__(self):
        pass

    def name(self) -> str:
        try:
            if psutil.WINDOWS:
                return subprocess.check_output(["wmic", "cpu", "get", "name"]).decode("utf-8").strip().split("\n")[1]
            elif psutil.LINUX:
                return (
                    subprocess.check_output(
                        "lscpu | sed -nr '/Model name/ s/  / /g; s/.*:\s*(.*) @ .*/\\1/p'",
                        shell=True,
                    )
                    .decode("utf-8")
                    .strip()
                )
        except Exception:
            return "Unknown CPU"

    def brand(self):
        return platform.processor()

    def uuid(self):
        try:
            if psutil.LINUX:
                return os.popen("hdparm -I /dev/sda | grep 'Serial Number'").read().split()[-1]
            elif psutil.WINDOWS:
                return wmi.WMI().Win32_ComputerSystemProduct()[0].UUID
        except Exception:
            return None

    def architecture(self):
        return platform.machine()

    def temperature(self, fahrenheit=False):
        if hasattr(psutil, "sensors_temperatures"):
            temp_readings = psutil.sensors_temperatures(fahrenheit=fahrenheit)["coretemp"]
            temp = []
            for reading in temp_readings:
                if "Core" in reading.label:
                    temp.append(reading.current)
            temp = sum(temp) / len(temp) if temp else None
            ret = {"Fahrenheit": temp} if fahrenheit else {"Celsius": temp}
        else:
            try:
                w = wmi.WMI("root\wmi")
                temp = w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature
                if fahrenheit:
                    ret = {"Fahrenheit": (temp / 10 - 32) * 5 / 9 + 273.15}
                else:
                    ret = {"Celsius": (temp / 10) - 273.15}
            except Exception:
                ret = {"Fahrenheit": None} if fahrenheit else {"Celsius": None}
        return ret

    def usage(self):
        mem_info = self.memory_info()
        return {
            "usage": psutil.cpu_percent(0.05),
            "memory_usage": mem_info["used"] / mem_info["total"] * 100,
        }

    def memory_info(self):
        v_mem = psutil.virtual_memory()
        return {
            "total": v_mem.total,
            "free": v_mem.available,
            "used": v_mem.total - v_mem.available,
        }

    def process_info(self):
        ret = []
        for _p in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_info"]):
            ret.append(
                {
                    "pid": _p.info["pid"],
                    "name": _p.info["name"],
                    "usage": _p.info["cpu_percent"],
                    "used_memory": _p.info["memory_info"].vms,
                }
            )
        return ret

    def to_proto(self, **kwargs):
        ret = self.summary(**kwargs)
        return CPUProtoBuilder.build_proto(**ret)
