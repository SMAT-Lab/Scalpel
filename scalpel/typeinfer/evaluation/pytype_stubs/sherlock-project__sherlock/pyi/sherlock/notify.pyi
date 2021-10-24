# (generated with --quick)

import colorama.ansi
from typing import Any

Fore: colorama.ansi.AnsiFore
QueryStatus: Any
Style: colorama.ansi.AnsiStyle

class QueryNotify:
    __doc__: str
    result: Any
    def __init__(self, result = ...) -> None: ...
    def __str__(self) -> str: ...
    def finish(self, message = ...) -> None: ...
    def start(self, message = ...) -> None: ...
    def update(self, result) -> None: ...

class QueryNotifyPrint(QueryNotify):
    __doc__: str
    color: Any
    print_all: Any
    result: Any
    verbose: Any
    def __init__(self, result = ..., verbose = ..., color = ..., print_all = ...) -> None: ...
    def __str__(self) -> str: ...
    def start(self, message) -> None: ...
    def update(self, result) -> None: ...

def init(autoreset: bool = ..., convert: bool = ..., strip: bool = ..., wrap: bool = ...) -> None: ...
