# (generated with --quick)

from typing import Any, Dict, NoReturn

class AuthPlugin(BasePlugin):
    __doc__: str
    auth_parse: bool
    auth_require: bool
    auth_type: None
    netrc_parse: bool
    prompt_password: bool
    raw_auth: None
    def get_auth(self, username = ..., password = ...) -> NoReturn: ...

class BasePlugin:
    description: None
    name: None
    package_name: None

class ConverterPlugin(BasePlugin):
    __doc__: str
    mime: Any
    def __init__(self, mime) -> None: ...
    def convert(self, content_bytes) -> NoReturn: ...
    @classmethod
    def supports(cls, mime) -> NoReturn: ...

class FormatterPlugin(BasePlugin):
    __doc__: str
    enabled: bool
    format_options: Any
    group_name: str
    kwargs: Dict[str, Any]
    def __init__(self, **kwargs) -> None: ...
    def format_body(self, content: str, mime: str) -> str: ...
    def format_headers(self, headers: str) -> str: ...

class TransportPlugin(BasePlugin):
    __doc__: str
    prefix: None
    def get_adapter(self) -> NoReturn: ...
