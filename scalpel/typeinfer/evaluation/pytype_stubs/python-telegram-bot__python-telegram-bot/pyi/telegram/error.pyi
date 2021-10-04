# (generated with --quick)

from typing import Any, Tuple

class BadRequest(NetworkError):
    __slots__ = []
    __doc__: str
    message: str

class ChatMigrated(TelegramError):
    __slots__ = ["new_chat_id"]
    __doc__: str
    message: Any
    new_chat_id: int
    def __init__(self, new_chat_id: int) -> None: ...
    def __reduce__(self) -> Tuple[type, Tuple[int]]: ...

class Conflict(TelegramError):
    __slots__ = []
    __doc__: str
    message: str
    def __reduce__(self) -> Tuple[type, Tuple[str]]: ...

class InvalidToken(TelegramError):
    __slots__ = []
    __doc__: str
    message: Any
    def __init__(self) -> None: ...
    def __reduce__(self) -> Tuple[type, tuple]: ...

class NetworkError(TelegramError):
    __slots__ = []
    __doc__: str
    message: str

class RetryAfter(TelegramError):
    __slots__ = ["retry_after"]
    __doc__: str
    message: Any
    retry_after: float
    def __init__(self, retry_after: int) -> None: ...
    def __reduce__(self) -> Tuple[type, Tuple[float]]: ...

class TelegramError(Exception):
    __slots__ = ["message"]
    __doc__: str
    message: str
    def __init__(self, message: str) -> None: ...
    def __reduce__(self) -> Tuple[type, Tuple[str]]: ...
    def __str__(self) -> str: ...

class TimedOut(NetworkError):
    __slots__ = []
    __doc__: str
    message: Any
    def __init__(self) -> None: ...
    def __reduce__(self) -> Tuple[type, tuple]: ...

class Unauthorized(TelegramError):
    __slots__ = []
    __doc__: str
    message: str

def _lstrip_str(in_s: str, lstr: str) -> str: ...
