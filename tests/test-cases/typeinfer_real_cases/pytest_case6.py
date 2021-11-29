'''
From pytest_nose.py
'''
from _pytest.config import hookimpl
from _pytest.fixtures import getfixturemarker
from _pytest.nodes import Item
from _pytest.python import Function
from _pytest.unittest import TestCaseFunction

def pytest_runtest_setup(item: Item) -> None:
    if not isinstance(item, Function):
        return
    # Don't do nose style setup/teardown on direct unittest style classes.
    if isinstance(item, TestCaseFunction):
        return

    # Capture the narrowed type of item for the teardown closure,
    # see https://github.com/python/mypy/issues/2608
    func = item

    call_optional(func.obj, "setup")
    func.addfinalizer(lambda: call_optional(func.obj, "teardown"))

    # NOTE: Module- and class-level fixtures are handled in python.py
    # with `pluginmanager.has_plugin("nose")` checks.
    # It would have been nicer to implement them outside of core, but
    # it's not straightforward.


