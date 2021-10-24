# (generated with --quick)

import collections
import requests.structures
from typing import Any, Generator, Tuple, Type

CaseInsensitiveDict: Type[requests.structures.CaseInsensitiveDict]
OrderedDict: Type[collections.OrderedDict]

class MultiValueOrderedDict(collections.OrderedDict):
    __doc__: str
    def __setitem__(self, key, value) -> None: ...
    def items(self) -> Generator[Tuple[Any, Any], Any, None]: ...

class MultipartRequestDataDict(MultiValueOrderedDict): ...

class RequestDataDict(MultiValueOrderedDict): ...

class RequestFilesDict(RequestDataDict): ...

class RequestHeadersDict(requests.structures.CaseInsensitiveDict):
    __doc__: str

class RequestJSONDataDict(collections.OrderedDict): ...

class RequestQueryParamsDict(MultiValueOrderedDict): ...
