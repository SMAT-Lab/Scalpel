# (generated with --quick)

import __future__

absolute_import: __future__._Feature
division: __future__._Feature
print_function: __future__._Feature
time: module
unicode_literals: __future__._Feature

class Timer:
    __doc__: str
    average_time: float
    calls: int
    diff: float
    start_time: float
    total_time: float
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def tic(self) -> None: ...
    def toc(self, average = ...) -> float: ...
