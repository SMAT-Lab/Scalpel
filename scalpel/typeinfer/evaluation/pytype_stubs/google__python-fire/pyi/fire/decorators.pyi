# (generated with --quick)

import __future__
from typing import Any, Callable

ACCEPTS_POSITIONAL_ARGS: str
FIRE_METADATA: str
FIRE_PARSE_FNS: str
absolute_import: __future__._Feature
division: __future__._Feature
inspect: module
print_function: __future__._Feature

def GetMetadata(fn) -> dict: ...
def GetParseFns(fn) -> dict: ...
def SetParseFn(fn, *arguments) -> Callable[[Any], Any]: ...
def SetParseFns(*positional, **named) -> Callable[[Any], Any]: ...
def _SetMetadata(fn, attribute, value) -> None: ...
