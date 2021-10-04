# (generated with --quick)

from typing import Any

sys: module

class APIConnectionError(APIError):
    _message: Any
    headers: Any
    http_body: Any
    http_status: Any
    json_body: Any
    request_id: Any

class APIError(Error):
    _message: Any
    headers: Any
    http_body: Any
    http_status: Any
    json_body: Any
    request_id: Any
    def __init__(self, message = ..., http_body = ..., http_status = ..., json_body = ..., headers = ...) -> None: ...
    def __str__(self) -> Any: ...
    def __unicode__(self) -> Any: ...

class AlreadyPendingCallError(Exception):
    __doc__: str
    name: Any
    def __init__(self, message, name) -> None: ...

class AuthenticationError(APIError):
    _message: Any
    headers: Any
    http_body: Any
    http_status: Any
    json_body: Any
    request_id: Any

class ClosedEnvironmentError(Exception):
    __doc__: str

class CustomSpaceError(Exception):
    __doc__: str

class DependencyNotInstalled(Error): ...

class DeprecatedEnv(Error):
    __doc__: str

class DoubleWrapperError(Error): ...

class Error(Exception): ...

class InvalidAction(Exception):
    __doc__: str

class InvalidFrame(Error): ...

class InvalidRequestError(APIError):
    _message: Any
    headers: Any
    http_body: Any
    http_status: Any
    json_body: Any
    param: Any
    request_id: Any
    def __init__(self, message, param, http_body = ..., http_status = ..., json_body = ..., headers = ...) -> None: ...

class NoAsyncCallError(Exception):
    __doc__: str
    name: Any
    def __init__(self, message, name) -> None: ...

class RateLimitError(APIError):
    _message: Any
    headers: Any
    http_body: Any
    http_status: Any
    json_body: Any
    request_id: Any

class ResetNeeded(Exception):
    __doc__: str

class ResetNotAllowed(Exception):
    __doc__: str

class RetriesExceededError(Error): ...

class Unregistered(Error):
    __doc__: str

class UnregisteredBenchmark(Unregistered):
    __doc__: str

class UnregisteredEnv(Unregistered):
    __doc__: str

class UnseedableEnv(Error):
    __doc__: str

class UnsupportedMode(Exception):
    __doc__: str

class VideoRecorderError(Error): ...

class WrapAfterConfigureError(Error): ...
