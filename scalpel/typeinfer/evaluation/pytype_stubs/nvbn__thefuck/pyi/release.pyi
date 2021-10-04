# (generated with --quick)

from typing import Any, Callable, Generator, IO, List, Mapping, Optional, Sequence, TextIO, Union

env: os._Environ[str]
lines: List[str]
os: module
re: module
sf: TextIO
version: Optional[str]

def call(args: Union[bytes, str, os.PathLike[Union[bytes, str]], Sequence[Union[bytes, str, os.PathLike[Union[bytes, str]]]]], bufsize: int = ..., executable: Optional[Union[bytes, str, os.PathLike[Union[bytes, str]]]] = ..., stdin: Optional[Union[int, IO]] = ..., stdout: Optional[Union[int, IO]] = ..., stderr: Optional[Union[int, IO]] = ..., preexec_fn: Optional[Callable[[], Any]] = ..., close_fds: bool = ..., shell: bool = ..., cwd: Optional[Union[bytes, str, os.PathLike[Union[bytes, str]]]] = ..., env: Optional[Mapping[Union[bytes, str], Union[bytes, str, os.PathLike[Union[bytes, str]]]]] = ..., universal_newlines: bool = ..., startupinfo = ..., creationflags: int = ..., restore_signals: bool = ..., start_new_session: bool = ..., pass_fds = ..., *, timeout: Optional[float] = ...) -> int: ...
def get_new_setup_py_lines() -> Generator[str, Any, None]: ...
