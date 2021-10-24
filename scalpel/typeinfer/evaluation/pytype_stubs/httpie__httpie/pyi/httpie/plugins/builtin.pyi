# (generated with --quick)

import httpie.plugins.base
import requests.auth
import requests.models
from typing import Optional, Type

AuthPlugin: Type[httpie.plugins.base.AuthPlugin]
requests: module

class BasicAuthPlugin(BuiltinAuthPlugin):
    auth_type: str
    name: str
    netrc_parse: bool
    def get_auth(self, username: str, password: str) -> HTTPBasicAuth: ...

class BuiltinAuthPlugin(httpie.plugins.base.AuthPlugin):
    package_name: str

class DigestAuthPlugin(BuiltinAuthPlugin):
    auth_type: str
    name: str
    netrc_parse: bool
    def get_auth(self, username: str, password: str) -> requests.auth.HTTPDigestAuth: ...

class HTTPBasicAuth(requests.auth.HTTPBasicAuth):
    def __call__(self, request: requests.models.PreparedRequest) -> requests.models.PreparedRequest: ...
    @staticmethod
    def make_header(username: str, password: str) -> str: ...

def b64encode(s: bytes, altchars: Optional[bytes] = ...) -> bytes: ...
