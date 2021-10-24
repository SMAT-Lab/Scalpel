# (generated with --quick)

import requests.adapters
from typing import Any, Dict, Type

AVAILABLE_SSL_VERSION_ARG_MAPPING: Dict[str, Any]
DEFAULT_CIPHERS: Any
DEFAULT_SSL_CIPHERS: Any
HTTPAdapter: Type[requests.adapters.HTTPAdapter]
SSL_VERSION_ARG_MAPPING: Dict[str, str]
create_urllib3_context: Any
resolve_ssl_version: Any
ssl: module

class HTTPieHTTPSAdapter(requests.adapters.HTTPAdapter):
    _ssl_context: ssl.SSLContext
    def __init__(self, verify: bool, ssl_version: str = ..., ciphers: str = ..., **kwargs) -> None: ...
    @staticmethod
    def _create_ssl_context(verify: bool, ssl_version: str = ..., ciphers: str = ...) -> ssl.SSLContext: ...
    def init_poolmanager(self, *args, **kwargs) -> Any: ...
    def proxy_manager_for(self, *args, **kwargs) -> Any: ...
