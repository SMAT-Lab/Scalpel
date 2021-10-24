# (generated with --quick)

import __future__
from typing import Any, Dict, Tuple

absolute_import: __future__._Feature
division: __future__._Feature
os: module
platform: module
subprocess: module
sys: module
unicode_literals: __future__._Feature

class Architecture:
    _ALL: list
    _ARCH: type
    _MACHINE_TO_ARCHITECTURE: Dict[str, Any]
    __doc__: str
    arm: Any
    ppc: Any
    x86: Any
    x86_64: Any
    @staticmethod
    def AllValues() -> list: ...
    @staticmethod
    def Current() -> Any: ...
    @staticmethod
    def FromId(architecture_id, error_on_unknown = ...) -> Any: ...

class Error(Exception):
    __doc__: str

class InvalidEnumValue(Error):
    __doc__: str
    def __init__(self, given, enum_type, options) -> None: ...

class OperatingSystem:
    CYGWIN: Any
    LINUX: Any
    MACOSX: Any
    MSYS: Any
    WINDOWS: Any
    _ALL: list
    _OS: type
    __doc__: str
    @staticmethod
    def AllValues() -> list: ...
    @staticmethod
    def Current() -> Any: ...
    @staticmethod
    def FromId(os_id, error_on_unknown = ...) -> Any: ...
    @staticmethod
    def IsWindows() -> bool: ...

class Platform:
    __doc__: str
    architecture: Any
    operating_system: Any
    def AsyncPopenArgs(self) -> Dict[str, int]: ...
    @staticmethod
    def Current(os_override = ..., arch_override = ...) -> Platform: ...
    def UserAgentFragment(self) -> str: ...
    def __init__(self, operating_system, architecture) -> None: ...
    def __str__(self) -> str: ...

class PythonVersion:
    ENV_VAR_MESSAGE: str
    MIN_REQUIRED_PY2_VERSION: Tuple[int, int]
    MIN_SUPPORTED_PY2_VERSION: Tuple[int, int]
    MIN_SUPPORTED_PY3_VERSION: Tuple[int, int]
    __doc__: str
    version: Any
    def IsCompatible(self, allow_py3 = ..., raise_exception = ...) -> bool: ...
    def SupportedVersionMessage(self, allow_py3) -> str: ...
    def __init__(self, version = ...) -> None: ...
