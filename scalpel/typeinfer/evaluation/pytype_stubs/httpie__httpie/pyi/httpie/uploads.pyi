# (generated with --quick)

import httpie.cli.dicts
import requests.models
from typing import Any, Callable, Iterable, Mapping, Sequence, Tuple, Type, TypeVar, Union

MultipartEncoder: Any
MultipartRequestDataDict: Type[httpie.cli.dicts.MultipartRequestDataDict]
RequestDataDict: Type[httpie.cli.dicts.RequestDataDict]
requests: module
zlib: module

AnyStr = TypeVar('AnyStr', str, bytes)

class ChunkedMultipartUploadStream:
    chunk_size: int
    encoder: Any
    def __init__(self, encoder) -> None: ...
    def __iter__(self) -> Iterable[Union[bytes, str]]: ...

class ChunkedUploadStream:
    callback: Callable
    stream: Iterable
    def __init__(self, stream: Iterable, callback: Callable) -> None: ...
    def __iter__(self) -> Iterable[Union[bytes, str]]: ...

def compress_request(request: requests.models.PreparedRequest, always: bool) -> None: ...
def get_multipart_data_and_content_type(data: httpie.cli.dicts.MultipartRequestDataDict, boundary: str = ..., content_type: str = ...) -> Tuple[Any, str]: ...
def prepare_request_body(body, body_read_callback: Callable[[bytes], bytes], content_length_header_value: int = ..., chunked = ..., offline = ...) -> Any: ...
def super_len(o) -> Any: ...
def urlencode(query: Union[Mapping, Sequence[Tuple[Any, Any]]], doseq: bool = ..., safe: AnyStr = ..., encoding: str = ..., errors: str = ..., quote_via: Callable[[str, AnyStr, str, str], str] = ...) -> str: ...
