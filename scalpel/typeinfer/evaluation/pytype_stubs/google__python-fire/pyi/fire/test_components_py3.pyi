# (generated with --quick)

from typing import Any, Dict, Tuple, TypeVar

asyncio: module
functools: module
lru_cache_decorated: functools._lru_cache_wrapper

_T0 = TypeVar('_T0')
_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')
_T3 = TypeVar('_T3')

class KeywordOnly:
    def double(self, *, count) -> Any: ...
    def triple(self, *, count) -> Any: ...
    def with_default(self, *, x = ...) -> None: ...

class LruCacheDecoratedMethod:
    lru_cache_in_class: functools._lru_cache_wrapper

class WithAsyncio:
    def double(self, count = ...) -> coroutine: ...

class WithDefaultsAndTypes:
    __doc__: str
    def double(self, count: float = ...) -> float: ...
    def get_int(self, value: int = ...) -> int: ...

class WithTypes:
    __doc__: str
    def double(self, count: float) -> float: ...
    def long_type(self, long_obj: Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[int]]]]]]]]]]]]) -> Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[Tuple[int]]]]]]]]]]]]: ...

def identity(arg1: _T0, arg2: int, arg3: _T1 = ..., arg4: int = ..., *arg5, arg6: _T2, arg7: int, arg8: _T3 = ..., arg9: int = ..., **arg10) -> Tuple[_T0, int, _T1, int, tuple, _T2, int, _T3, int, Dict[str, Any]]: ...
