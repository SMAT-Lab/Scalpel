# (generated with --quick)

import httpie.plugins.base
from typing import Any, Type

FormatterPlugin: Type[httpie.plugins.base.FormatterPlugin]

class HeadersFormatter(httpie.plugins.base.FormatterPlugin):
    enabled: Any
    def __init__(self, **kwargs) -> None: ...
    def format_headers(self, headers: str) -> str: ...
