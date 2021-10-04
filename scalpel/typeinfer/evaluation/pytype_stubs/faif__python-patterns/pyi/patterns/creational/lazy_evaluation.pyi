# (generated with --quick)

from typing import Annotated, Any

doctest: module
functools: module

class Person:
    call_count2: int
    name: Any
    occupation: Any
    parents: Annotated[Any, 'property']
    relatives: Any
    def __init__(self, name, occupation) -> None: ...

class lazy_property:
    function: Any
    def __get__(self, obj, type_) -> Any: ...
    def __init__(self, function) -> None: ...

def lazy_property2(fn) -> property: ...
def main() -> None: ...
