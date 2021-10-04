# (generated with --quick)

import builtins
import collections
import http.cookies
import io
import json.decoder
import simplejson.scanner
import typing
from typing import Any, Dict, List, Optional, Sequence, Tuple, Type, TypeVar, Union, overload
import urllib.parse

Callable: Type[typing.Callable]
JSONDecodeError: Type[Union[json.decoder.JSONDecodeError, simplejson.scanner.JSONDecodeError]]
Mapping: Type[typing.Mapping]
Morsel: Type[http.cookies.Morsel]
MutableMapping: Type[typing.MutableMapping]
OrderedDict: Type[collections.OrderedDict]
StringIO: Type[io.StringIO]
_ver: Tuple[int, int, int, builtins.str, int]
basestring: Tuple[Type[builtins.str], Type[builtins.bytes]]
builtin_str: Type[builtins.str]
bytes: Type[builtins.bytes]
chardet: Any
cookielib: module
getproxies_environment: Any
has_simplejson: bool
integer_types: Tuple[Type[int]]
is_py2: bool
is_py3: bool
json: module
numeric_types: Tuple[Type[int], Type[float]]
proxy_bypass_environment: Any
str: Type[builtins.str]
sys: module

AnyStr = TypeVar('AnyStr', builtins.str, builtins.bytes)

def getproxies() -> Dict[builtins.str, builtins.str]: ...
def parse_http_list(s: builtins.str) -> List[builtins.str]: ...
def proxy_bypass(host: builtins.str, proxies: Optional[typing.Mapping[builtins.str, builtins.str]] = ...) -> Any: ...
@overload
def quote(string: builtins.str, safe: Union[bytearray, builtins.bytes, memoryview, builtins.str] = ..., encoding: Optional[builtins.str] = ..., errors: Optional[builtins.str] = ...) -> builtins.str: ...
@overload
def quote(string: Union[bytearray, builtins.bytes, memoryview], safe: Union[bytearray, builtins.bytes, memoryview, builtins.str] = ...) -> builtins.str: ...
@overload
def quote_plus(string: builtins.str, safe: Union[bytearray, builtins.bytes, memoryview, builtins.str] = ..., encoding: Optional[builtins.str] = ..., errors: Optional[builtins.str] = ...) -> builtins.str: ...
@overload
def quote_plus(string: Union[bytearray, builtins.bytes, memoryview], safe: Union[bytearray, builtins.bytes, memoryview, builtins.str] = ...) -> builtins.str: ...
def unquote(string: builtins.str, encoding: builtins.str = ..., errors: builtins.str = ...) -> builtins.str: ...
def unquote_plus(string: builtins.str, encoding: builtins.str = ..., errors: builtins.str = ...) -> builtins.str: ...
@overload
def urldefrag(url: builtins.str) -> urllib.parse.DefragResult: ...
@overload
def urldefrag(url: Optional[Union[bytearray, builtins.bytes, memoryview]]) -> urllib.parse.DefragResultBytes: ...
def urlencode(query: Union[typing.Mapping, Sequence[Tuple[Any, Any]]], doseq: bool = ..., safe: AnyStr = ..., encoding: builtins.str = ..., errors: builtins.str = ..., quote_via: typing.Callable[[builtins.str, AnyStr, builtins.str, builtins.str], builtins.str] = ...) -> builtins.str: ...
def urljoin(base: AnyStr, url: Optional[AnyStr], allow_fragments: bool = ...) -> AnyStr: ...
@overload
def urlparse(url: builtins.str, scheme: Optional[builtins.str] = ..., allow_fragments: bool = ...) -> urllib.parse.ParseResult: ...
@overload
def urlparse(url: Optional[Union[bytearray, builtins.bytes, memoryview]], scheme: Optional[Union[bytearray, builtins.bytes, memoryview]] = ..., allow_fragments: bool = ...) -> urllib.parse.ParseResultBytes: ...
@overload
def urlsplit(url: builtins.str, scheme: Optional[builtins.str] = ..., allow_fragments: bool = ...) -> urllib.parse.SplitResult: ...
@overload
def urlsplit(url: Optional[Union[bytearray, builtins.bytes, memoryview]], scheme: Optional[Union[bytearray, builtins.bytes, memoryview]] = ..., allow_fragments: bool = ...) -> urllib.parse.SplitResultBytes: ...
def urlunparse(components: Union[Sequence[Optional[AnyStr]], Tuple[Optional[AnyStr], Optional[AnyStr], Optional[AnyStr], Optional[AnyStr], Optional[AnyStr], Optional[AnyStr]]]) -> AnyStr: ...
