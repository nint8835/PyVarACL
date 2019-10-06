from typing import Any
from types import FrameType
from dataclasses import dataclass
import inspect

from .utils import get_frame_function, get_caller


class ProtectedClass(object):
    _acl = []

    def _validate_acl(self, caller_info, attribute, attribute_name, action) -> bool:
        for entry in self._acl:
            if all(
                caller_info[key] in entry["targets"][key]
                for key in entry["targets"].keys()
            ) and entry["filter"](attribute, attribute_name, action):
                return entry["allow"]
        return False

    def __getattribute__(self, name: str):
        caller_frame = inspect.currentframe().f_back
        caller_info = get_caller(caller_frame)

        attribute = super().__getattribute__(name)

        if caller_info["instance"] == self:
            return attribute

        if self._validate_acl(caller_info, attribute, name, "read"):
            return attribute

        return None

    def __setattr__(self, name: str, value: Any):
        caller_frame = inspect.currentframe().f_back
        caller_info = get_caller(caller_frame)

        if caller_info["instance"] == self:
            super().__setattr__(name, value)

        if self._validate_acl(caller_info, None, name, "read"):
            super().__setattr__(name, value)
