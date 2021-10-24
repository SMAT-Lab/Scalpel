# (generated with --quick)

from typing import TypeVar, Union

BLACK: int
BLACK_BACKGROUND: int
BLUE: int
BLUE_BACKGROUND: int
BOLD: int
CYAN: int
CYAN_BACKGROUND: int
DARK_GRAY: int
DARK_GRAY_BACKGROUND: int
DEFAULT: int
DEFAULT_BACKGROUND: int
GREEN: int
GREEN_BACKGROUND: int
IS_ANSI_TERMINAL: bool
LIGHT_BLUE: int
LIGHT_BLUE_BACKGROUND: int
LIGHT_CYAN: int
LIGHT_CYAN_BACKGROUND: int
LIGHT_GRAY: int
LIGHT_GRAY_BACKGROUND: int
LIGHT_GREEN: int
LIGHT_GREEN_BACKGROUND: int
LIGHT_MAGENTA: int
LIGHT_MAGENTA_BACKGROUND: int
LIGHT_RED: int
LIGHT_RED_BACKGROUND: int
LIGHT_YELLOW: int
LIGHT_YELLOW_BACKGROUND: int
MAGENTA: int
MAGENTA_BACKGROUND: int
NEGATIVE: int
NO_BOLD: int
NO_UNDERLINE: int
POSITIVE: int
RED: int
RED_BACKGROUND: int
RESET: int
TERM: str
UNDERLINE: int
WHITE: int
WHITE_BACKGROUND: int
YELLOW: int
YELLOW_BACKGROUND: int
os: module
script_name: str
sys: module

_T0 = TypeVar('_T0')

def d(message) -> None: ...
def e(message, exit_code = ...) -> None: ...
def i(message) -> None: ...
def print_err(text, *colors) -> None: ...
def print_log(text, *colors) -> None: ...
def println(text, *colors) -> None: ...
def sprint(text: _T0, *colors) -> Union[str, _T0]: ...
def w(message) -> None: ...
def wtf(message, exit_code = ...) -> None: ...
def yes_or_no(message) -> bool: ...
