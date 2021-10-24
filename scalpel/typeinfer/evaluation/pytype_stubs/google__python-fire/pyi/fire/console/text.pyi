# (generated with --quick)

import __future__
from typing import Annotated, Any, TypeVar

absolute_import: __future__._Feature
division: __future__._Feature
enum: module
unicode_literals: __future__._Feature

_TTypedText = TypeVar('_TTypedText', bound=TypedText)

class TextAttributes:
    __doc__: str
    _attrs: Any
    _color: Any
    _format_str: Any
    attrs: Annotated[Any, 'property']
    color: Annotated[Any, 'property']
    format_str: Annotated[Any, 'property']
    def __init__(self, format_str = ..., color = ..., attrs = ...) -> None: ...

class TextTypes(_TextTypes):
    COMMAND: int
    INFO: int
    OUTPUT: int
    PT_FAILURE: int
    PT_SUCCESS: int
    RESOURCE_NAME: int
    URI: int
    URL: int
    USER_INPUT: int
    __doc__: str

class TypedText:
    __doc__: str
    text_type: Any
    texts: Any
    def __add__(self: _TTypedText, other) -> _TTypedText: ...
    def __init__(self, texts, text_type = ...) -> None: ...
    def __len__(self) -> int: ...
    def __radd__(self: _TTypedText, other) -> _TTypedText: ...

class _TextTypes(enum.Enum):
    __doc__: str
    def __call__(self, *args) -> TypedText: ...
