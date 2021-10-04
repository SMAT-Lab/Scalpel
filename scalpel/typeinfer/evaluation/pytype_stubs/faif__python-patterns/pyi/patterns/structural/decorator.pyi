# (generated with --quick)

from typing import Any

doctest: module

class BoldWrapper(TextTag):
    __doc__: str
    _wrapped: Any
    def __init__(self, wrapped) -> None: ...
    def render(self) -> str: ...

class ItalicWrapper(TextTag):
    __doc__: str
    _wrapped: Any
    def __init__(self, wrapped) -> None: ...
    def render(self) -> str: ...

class TextTag:
    __doc__: str
    _text: Any
    def __init__(self, text) -> None: ...
    def render(self) -> Any: ...

def main() -> None: ...
