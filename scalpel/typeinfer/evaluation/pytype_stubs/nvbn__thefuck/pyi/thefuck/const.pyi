# (generated with --quick)

from typing import Any, Dict, List, Optional, Union

ACTION_ABORT: _GenConst
ACTION_NEXT: _GenConst
ACTION_PREVIOUS: _GenConst
ACTION_SELECT: _GenConst
ALL_ENABLED: _GenConst
ARGUMENT_PLACEHOLDER: str
CONFIGURATION_TIMEOUT: int
DEFAULT_PRIORITY: int
DEFAULT_RULES: List[_GenConst]
DEFAULT_SETTINGS: Dict[str, Optional[Union[int, Dict[str, str], List[Union[_GenConst, str]]]]]
DIFF_WITH_ALIAS: float
ENV_TO_ATTR: Dict[str, str]
KEY_CTRL_C: _GenConst
KEY_CTRL_N: _GenConst
KEY_CTRL_P: _GenConst
KEY_DOWN: _GenConst
KEY_MAPPING: Dict[str, _GenConst]
KEY_UP: _GenConst
LOG_SIZE_IN_BYTES: int
LOG_SIZE_TO_CLEAN: int
SETTINGS_HEADER: str
SHELL_LOGGER_LIMIT: int
SHELL_LOGGER_SOCKET_ENV: str
USER_COMMAND_MARK: str

class _GenConst:
    _name: Any
    def __init__(self, name) -> None: ...
    def __repr__(self) -> str: ...
