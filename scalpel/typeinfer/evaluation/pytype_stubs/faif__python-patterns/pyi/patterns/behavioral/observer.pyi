# (generated with --quick)

import __future__
import contextlib
from typing import Annotated, List, Optional, Protocol, Type

annotations: __future__._Feature
doctest: module
suppress: Type[contextlib.suppress]

class Data(Subject):
    _data: int
    _observers: List[nothing]
    data: Annotated[int, 'property']
    name: str
    def __init__(self, name: str = ...) -> None: ...

class DecimalViewer:
    def update(self, subject: Data) -> None: ...

class HexViewer:
    def update(self, subject: Data) -> None: ...

class Observer(Protocol):
    def update(self, subject: Subject) -> None: ...

class Subject:
    _observers: List[Observer]
    def __init__(self) -> None: ...
    def attach(self, observer: Observer) -> None: ...
    def detach(self, observer: Observer) -> None: ...
    def notify(self, modifier: Optional[Observer] = ...) -> None: ...

def main() -> None: ...
