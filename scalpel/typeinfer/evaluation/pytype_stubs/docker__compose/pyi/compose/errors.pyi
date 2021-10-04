# (generated with --quick)

from typing import Any

class CompletedUnsuccessfully(Exception):
    msg: str
    def __init__(self, container_id, exit_code) -> None: ...

class HealthCheckException(Exception):
    msg: Any
    def __init__(self, reason) -> None: ...

class HealthCheckFailed(HealthCheckException):
    msg: str
    def __init__(self, container_id) -> None: ...

class NoHealthCheckConfigured(HealthCheckException):
    msg: str
    def __init__(self, service_name) -> None: ...

class OperationFailedError(Exception):
    msg: Any
    def __init__(self, reason) -> None: ...

class StreamParseError(RuntimeError):
    msg: Any
    def __init__(self, reason) -> None: ...
