# (generated with --quick)

import enum
from typing import Type, TypeVar

IntEnum: Type[enum.IntEnum]

_EnumType = TypeVar('_EnumType', bound=Type[enum.Enum])

class ExitStatus(enum.IntEnum):
    ERROR: int
    ERROR_CTRL_C: int
    ERROR_HTTP_3XX: int
    ERROR_HTTP_4XX: int
    ERROR_HTTP_5XX: int
    ERROR_TIMEOUT: int
    ERROR_TOO_MANY_REDIRECTS: int
    PLUGIN_ERROR: int
    SUCCESS: int
    __doc__: str

def http_status_to_exit_status(http_status: int, follow = ...) -> ExitStatus: ...
def unique(enumeration: _EnumType) -> _EnumType: ...
