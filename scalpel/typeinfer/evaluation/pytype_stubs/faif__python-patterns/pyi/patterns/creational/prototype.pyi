# (generated with --quick)

from typing import Dict, TypeVar

doctest: module

_TPrototype = TypeVar('_TPrototype', bound=Prototype)

class Prototype:
    value: str
    def __init__(self, value: str = ..., **attrs) -> None: ...
    def clone(self: _TPrototype, **attrs) -> _TPrototype: ...

class PrototypeDispatcher:
    _objects: Dict[str, Prototype]
    def __init__(self) -> None: ...
    def get_objects(self) -> Dict[str, Prototype]: ...
    def register_object(self, name: str, obj: Prototype) -> None: ...
    def unregister_object(self, name: str) -> None: ...

def main() -> None: ...