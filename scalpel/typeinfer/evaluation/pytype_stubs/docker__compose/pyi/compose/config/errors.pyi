# (generated with --quick)

from typing import Annotated, Any

VERSION_EXPLANATION: str

class CircularReference(ConfigurationError):
    msg: Annotated[str, 'property']
    trail: Any
    def __init__(self, trail) -> None: ...

class ComposeFileNotFound(ConfigurationError):
    msg: str
    def __init__(self, supported_filenames) -> None: ...

class ConfigurationError(Exception):
    msg: Any
    def __init__(self, msg) -> None: ...
    def __str__(self) -> Any: ...

class DependencyError(ConfigurationError):
    msg: Any

class DuplicateOverrideFileFound(ConfigurationError):
    msg: str
    override_filenames: Any
    def __init__(self, override_filenames) -> None: ...

class EnvFileNotFound(ConfigurationError):
    msg: Any
