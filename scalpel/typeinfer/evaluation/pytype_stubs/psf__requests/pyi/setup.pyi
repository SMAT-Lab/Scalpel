# (generated with --quick)

import codecs
from typing import Any, Dict, List, NoReturn, Optional, Tuple

TestCommand: Any
about: Dict[nothing, nothing]
f: codecs.StreamReaderWriter
here: str
os: module
packages: List[str]
readme: str
requires: List[str]
setup: Any
sys: module
test_requirements: List[str]

class PyTest(Any):
    pytest_args: List[str]
    test_args: List[nothing]
    test_suite: bool
    user_options: List[Tuple[str, str, str]]
    def finalize_options(self) -> None: ...
    def initialize_options(self) -> None: ...
    def run_tests(self) -> NoReturn: ...

