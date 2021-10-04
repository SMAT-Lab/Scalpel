# (generated with --quick)

import contextlib
from typing import Callable, Iterator, Optional, TypeVar, Union

atomic_write: Callable[..., contextlib._GeneratorContextManager]
os: module
sys: module

_T = TypeVar('_T')

def contextmanager(func: Callable[..., Iterator[_T]]) -> Callable[..., contextlib._GeneratorContextManager[_T]]: ...
def replace(src: Union[bytes, str, os.PathLike[Union[bytes, str]]], dst: Union[bytes, str, os.PathLike[Union[bytes, str]]], *, src_dir_fd: Optional[int] = ..., dst_dir_fd: Optional[int] = ...) -> None: ...
