# (generated with --quick)

import threading
from typing import Any, Callable, Dict, List, Optional, Type, Union, overload

Event: Type[threading.Event]
Thread: Type[threading.Thread]
__all__: List[str]
atexit: module

class TMonitor(threading.Thread):
    __doc__: str
    _test: Dict[nothing, nothing]
    _time: Callable[[], float]
    daemon: bool
    sleep_interval: Any
    tqdm_cls: Any
    was_killed: threading.Event
    woken: Union[float, int]
    def __init__(self, tqdm_cls, sleep_interval) -> None: ...
    def exit(self) -> bool: ...
    def get_instances(self) -> list: ...
    def report(self) -> bool: ...
    def run(self) -> None: ...

class TqdmSynchronisationWarning(RuntimeWarning):
    __doc__: str

def current_thread() -> threading.Thread: ...
def time() -> float: ...
@overload
def warn(message: Warning, category = ..., stacklevel: int = ..., source = ...) -> None: ...
@overload
def warn(message: str, category: Optional[Type[Warning]] = ..., stacklevel: int = ..., source = ...) -> None: ...
