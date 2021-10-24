# (generated with --quick)

from typing import Iterator, Set, TypeVar

excluded: Set[str]
importlib: module
inspect: module
os: module

AnyStr = TypeVar('AnyStr', str, bytes)

def get_slots(_class) -> list: ...
def iglob(pathname: AnyStr, *, recursive: bool = ...) -> Iterator[AnyStr]: ...
def test_class_has_slots_and_dict(mro_slots) -> None: ...
