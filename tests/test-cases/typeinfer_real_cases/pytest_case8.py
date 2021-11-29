'''
From pytest_unittest.py
'''

import sys
import traceback
import types
from typing import Any
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TYPE_CHECKING
from typing import Union

import _pytest._code
import pytest
from _pytest.compat import getimfunc
from _pytest.compat import is_async_function
from _pytest.config import hookimpl
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Collector
from _pytest.nodes import Item
from _pytest.outcomes import exit
from _pytest.outcomes import fail
from _pytest.outcomes import skip
from _pytest.outcomes import xfail
from _pytest.python import Class
from _pytest.python import Function
from _pytest.python import PyCollector
from _pytest.runner import CallInfo
from _pytest.scope import Scope


def setup(self) -> None:
    # A bound method to be called during teardown() if set (see 'runtest()').
    self._explicit_tearDown: Optional[Callable[[], None]] = None
    assert self.parent is not None
    self._testcase = self.parent.obj(self.name)  # type: ignore[attr-defined]
    self._obj = getattr(self._testcase, self.name)
    if hasattr(self, "_request"):
        self._request._fillfixtures()