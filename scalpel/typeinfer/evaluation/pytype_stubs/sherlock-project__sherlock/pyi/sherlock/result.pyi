# (generated with --quick)

import enum
from typing import Any, Type

Enum: Type[enum.Enum]

class QueryResult:
    __doc__: str
    context: Any
    query_time: Any
    site_name: Any
    site_url_user: Any
    status: Any
    username: Any
    def __init__(self, username, site_name, site_url_user, status, query_time = ..., context = ...) -> None: ...
    def __str__(self) -> str: ...

class QueryStatus(enum.Enum):
    AVAILABLE: str
    CLAIMED: str
    ILLEGAL: str
    UNKNOWN: str
    __doc__: str
    def __str__(self) -> Any: ...
