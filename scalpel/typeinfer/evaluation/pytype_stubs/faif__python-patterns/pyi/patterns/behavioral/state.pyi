# (generated with --quick)

from typing import Any, List, Union

doctest: module

class AmState(State):
    name: str
    pos: int
    radio: Any
    stations: List[str]
    def __init__(self, radio) -> None: ...
    def toggle_amfm(self) -> None: ...

class FmState(State):
    name: str
    pos: int
    radio: Any
    stations: List[str]
    def __init__(self, radio) -> None: ...
    def toggle_amfm(self) -> None: ...

class Radio:
    __doc__: str
    amstate: AmState
    fmstate: FmState
    state: Union[AmState, FmState]
    def __init__(self) -> None: ...
    def scan(self) -> None: ...
    def toggle_amfm(self) -> None: ...

class State:
    __doc__: str
    pos: Any
    def scan(self) -> None: ...

def main() -> None: ...
