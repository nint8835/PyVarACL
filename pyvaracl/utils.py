import gc
import inspect
from types import FrameType
from typing import Any, Callable, Optional, Dict


def get_frame_function(frame: FrameType) -> Optional[Callable[..., Any]]:
    return next(
        (obj for obj in gc.get_referrers(frame.f_code) if inspect.isfunction(obj)), None
    )


def get_caller(frame: FrameType) -> Dict[str, Any]:
    function = get_frame_function(frame)
    instance = None
    if function is not None:
        arg_spec = inspect.getfullargspec(function)
        if "self" in arg_spec.args:
            instance = frame.f_locals["self"]
    return {
        "function": function,
        "module": inspect.getmodule(function),
        "instance": instance,
    }

