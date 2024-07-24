from __future__ import annotations

import os
import platform
import subprocess

import psutil

from monitor.reader.base import DeviceReader
from monitor.reader.proto import CPUProtoBuilder

if psutil.WINDOWS:
    import pythoncom
    import wmi

    pythoncom.CoInitialize()


class CPUReader(DeviceReader):
    _basic_info_list = [
        "name",
        "uuid",
        "architecture",
        "brand",
    ]
    _matrix_info_list = [
        "temperature",
        "usage",
        "memory_info",
    ]

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
            return "Unknown CPU"
        except Exception:
            return "Unknown CPU"

    def brand(self) -> str:
        return platform.processor()

    def uuid(self) -> str:
        try:
            if psutil.LINUX:
                return os.popen("hdparm -I /dev/sda | grep 'Serial Number'").read().split()[-1]
            elif psutil.WINDOWS:
                return wmi.WMI().Win32_ComputerSystemProduct()[0].UUID
        except Exception:
            return None

    def architecture(self) -> str:
        return platform.machine()

    def temperature(self, fahrenheit: bool = False) -> dict[str, float]:
        if hasattr(psutil, "sensors_temperatures"):
            temp_readings = psutil.sensors_temperatures(fahrenheit=fahrenheit)["coretemp"]
            temp = list(map(lambda x: x.current, filter(lambda x: "Core" in x.label, temp_readings)))
            temp = sum(temp) / len(temp) if temp else None
            ret = {"Fahrenheit" if fahrenheit else "Celsius": temp}
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

    def usage(self) -> dict[str, float]:
        mem_info = self.memory_info()
        return {
            "usage": psutil.cpu_percent(0.05),
            "memory_usage": mem_info["used"] / mem_info["total"] * 100,
        }

    def memory_info(self) -> dict[str, int]:
        v_mem = psutil.virtual_memory()
        return {
            "total": v_mem.total,
            "free": v_mem.available,
            "used": v_mem.total - v_mem.available,
        }

    def process_info(self) -> list[dict[str, int]]:
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

    def to_proto(
        self,
        basic_info: bool = True,
        matrix_info: bool = True,
    ) -> CPUProtoBuilder:
        ret = self.summary(basic_info=basic_info, matrix_info=matrix_info)
        return CPUProtoBuilder.build_proto(**ret)
