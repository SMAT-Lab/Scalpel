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


def fixture(self, request: FixtureRequest) -> Generator[None, None, None]:
    if _is_skipped(self):
        reason = self.__unittest_skip_why__
        raise pytest.skip.Exception(reason, _use_item_location=True)
    if setup is not None:
        try:
            if pass_self:
                setup(self, request.function)
            else:
                setup()
        # unittest does not call the cleanup function for every BaseException, so we
        # follow this here.
        except Exception:
            if pass_self:
                cleanup(self)
            else:
                cleanup()

            raise
    yield
    try:
        if teardown is not None:
            if pass_self:
                teardown(self, request.function)
            else:
                teardown()
    finally:
        if pass_self:
            cleanup(self)
        else:
            cleanup()


return fixture