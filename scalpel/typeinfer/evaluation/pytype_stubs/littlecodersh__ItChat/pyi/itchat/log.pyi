# (generated with --quick)

from typing import Any, List, Optional, TextIO

logging: module
ls: LogSystem

class LogSystem:
    cmdHandler: logging.StreamHandler[TextIO]
    fileHandler: Optional[logging.FileHandler]
    handlerList: List[nothing]
    logger: logging.Logger
    loggingFile: Any
    loggingLevel: Any
    showOnCmd: Any
    def __init__(self) -> None: ...
    def set_logging(self, showOnCmd = ..., loggingFile = ..., loggingLevel = ...) -> None: ...

def set_logging(showOnCmd = ..., loggingFile = ..., loggingLevel = ...) -> None: ...
