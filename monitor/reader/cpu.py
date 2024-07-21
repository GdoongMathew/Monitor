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
