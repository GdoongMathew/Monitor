from __future__ import annotations

from abc import abstractmethod
from typing import Any


class DeviceReader:
    _basic_info_list = []
    _matrix_info_list = []

    def summary(
        self,
        basic_info: bool = True,
        matrix_info: bool = True,
    ) -> dict[str, Any]:
        # gathering information
        _info_list = []
        if not basic_info and not matrix_info:
            raise ValueError("Either one of basic_info or matrix_info should be True")
        if basic_info:
            _info_list.extend(self._basic_info_list)
        if matrix_info:
            _info_list.extend(self._matrix_info_list)

        return {_info: getattr(self, _info)() for _info in _info_list}

    def name(self) -> str:
        return "Unknown Device"

    @abstractmethod
    def temperature(self) -> dict[str, float]:
        raise NotImplementedError

    @abstractmethod
    def memory_info(self):
        raise NotImplementedError

    @abstractmethod
    def to_proto(self, **kwargs):
        raise NotImplementedError
