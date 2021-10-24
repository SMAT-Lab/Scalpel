# (generated with --quick)

from typing import Optional, TypeVar

RTMPDUMP: Optional[str]
os: module
subprocess: module

_T0 = TypeVar('_T0')

def download_rtmpdump_stream(url, title, ext, params = ..., output_dir = ...) -> None: ...
def get_usable_rtmpdump(cmd: _T0) -> Optional[_T0]: ...
def has_rtmpdump_installed() -> bool: ...
def play_rtmpdump_stream(player, url, params = ...) -> None: ...
