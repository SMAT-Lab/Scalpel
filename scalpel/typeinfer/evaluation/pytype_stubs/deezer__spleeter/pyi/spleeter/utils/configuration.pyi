# (generated with --quick)

import os
import spleeter
from typing import Any, Type, Union

SpleeterError: Type[spleeter.SpleeterError]
_EMBEDDED_CONFIGURATION_PREFIX: str
__author__: str
__email__: str
__license__: str
json: module
loader: Any
resources: module

def exists(path: Union[bytes, str, os.PathLike[Union[bytes, str]]]) -> bool: ...
def load_configuration(descriptor: str) -> dict: ...
