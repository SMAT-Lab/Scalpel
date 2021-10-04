# (generated with --quick)

from typing import Optional, TypeVar, Union

REPO_ROOT: str
os: module
re: module

_T1 = TypeVar('_T1')

def update_init_py_version(version) -> None: ...
def update_run_sh_version(version) -> None: ...
def yesno(prompt, default: _T1 = ...) -> Optional[Union[bool, _T1]]: ...
