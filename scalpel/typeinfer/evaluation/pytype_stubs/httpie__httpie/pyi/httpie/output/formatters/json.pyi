# (generated with --quick)

import httpie.plugins.base
from typing import Any, Type

FormatterPlugin: Type[httpie.plugins.base.FormatterPlugin]
json: module

class JSONFormatter(httpie.plugins.base.FormatterPlugin):
    enabled: Any
    def __init__(self, **kwargs) -> None: ...
    def format_body(self, body: str, mime: str) -> str: ...
