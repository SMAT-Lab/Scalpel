# (generated with --quick)

from typing import Any, Optional, TypeVar

doctest: module

_T0 = TypeVar('_T0')
_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')

class GraphSearch:
    __doc__: str
    graph: Any
    def __init__(self, graph) -> None: ...
    def find_all_paths_dfs(self, start: _T0, end, path: _T2 = ...) -> list: ...
    def find_path_dfs(self, start, end, path = ...) -> Any: ...
    def find_shortest_path_bfs(self, start: _T0, end: _T1) -> Optional[list]: ...
    def find_shortest_path_dfs(self, start, end, path = ...) -> Any: ...

def main() -> None: ...
