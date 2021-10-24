# (generated with --quick)

import __future__
from typing import Any

absolute_import: __future__._Feature
division: __future__._Feature
print_function: __future__._Feature
unicode_literals: __future__._Feature

class AttrDict(dict):
    IMMUTABLE: str
    def __getattr__(self, name) -> Any: ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __setattr__(self, name, value) -> None: ...
    def immutable(self, is_immutable) -> None: ...
    def is_immutable(self) -> Any: ...
