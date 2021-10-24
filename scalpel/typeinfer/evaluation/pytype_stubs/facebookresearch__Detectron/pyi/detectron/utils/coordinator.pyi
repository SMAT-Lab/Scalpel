# (generated with --quick)

import __future__
from typing import Any, Callable

Queue: module
absolute_import: __future__._Feature
contextlib: module
division: __future__._Feature
log: logging.Logger
logging: module
print_function: __future__._Feature
threading: module
traceback: module
unicode_literals: __future__._Feature

class Coordinator:
    _event: threading.Event
    stop_on_exception: Callable[..., contextlib._GeneratorContextManager]
    def __init__(self) -> None: ...
    def request_stop(self) -> None: ...
    def should_stop(self) -> bool: ...
    def wait_for_stop(self) -> bool: ...

def coordinated_get(coordinator, queue) -> Any: ...
def coordinated_put(coordinator, queue, element) -> None: ...
