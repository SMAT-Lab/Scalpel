# (generated with --quick)

import pathlib
from typing import Annotated, Dict, List, Type, Union

DEFAULT_CONFIG_DIR: pathlib.Path
DEFAULT_CONFIG_DIRNAME: str
DEFAULT_RELATIVE_LEGACY_CONFIG_DIR: pathlib.Path
DEFAULT_RELATIVE_XDG_CONFIG_HOME: pathlib.Path
DEFAULT_WINDOWS_CONFIG_DIR: pathlib.Path
ENV_HTTPIE_CONFIG_DIR: str
ENV_XDG_CONFIG_HOME: str
Path: Type[pathlib.Path]
UTF8: str
__version__: str
is_windows: bool
json: module
os: module

class BaseConfigDict(dict):
    about: None
    helpurl: None
    name: None
    path: pathlib.Path
    def __init__(self, path: pathlib.Path) -> None: ...
    def ensure_directory(self) -> None: ...
    def is_new(self) -> bool: ...
    def load(self) -> None: ...
    def save(self) -> None: ...

class Config(BaseConfigDict):
    DEFAULTS: Dict[str, List[nothing]]
    FILENAME: str
    default_options: Annotated[list, 'property']
    directory: pathlib.Path
    path: pathlib.Path
    def __init__(self, directory: Union[str, pathlib.Path] = ...) -> None: ...

class ConfigFileError(Exception): ...

def get_default_config_dir() -> pathlib.Path: ...
