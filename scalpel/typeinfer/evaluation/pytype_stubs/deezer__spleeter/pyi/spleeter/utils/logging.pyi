# (generated with --quick)

import os
from typing import Any

__author__: str
__email__: str
__license__: str
echo: Any
environ: os._Environ[str]
formatter: logging.Formatter
handler: TyperLoggerHandler
logger: logging.Logger
logging: module
warnings: module

class TyperLoggerHandler(logging.Handler):
    __doc__: str
    def emit(self, record: logging.LogRecord) -> None: ...

def configure_logger(verbose: bool) -> None: ...
