# (generated with --quick)

import itertools
from typing import Any, Type, TypeVar, Union

chain: Type[itertools.chain]
functools: module
logging: module
pprint: module

_T0 = TypeVar('_T0')

class VerboseProxy:
    __doc__: str
    log: logging.Logger
    max_lines: Any
    obj: Any
    obj_name: Any
    def __getattr__(self, name) -> Any: ...
    def __init__(self, obj_name, obj, log_name = ..., max_lines = ...) -> None: ...
    def proxy_callable(self, call_name, *args, **kwargs) -> Any: ...

def format_call(args, kwargs) -> str: ...
def format_return(result: _T0, max_lines) -> Union[str, _T0]: ...
