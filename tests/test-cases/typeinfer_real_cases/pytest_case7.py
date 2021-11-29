'''
From pytest_nose.py
'''
from _pytest.config import hookimpl
from _pytest.fixtures import getfixturemarker
from _pytest.nodes import Item
from _pytest.python import Function
from _pytest.unittest import TestCaseFunction

def call_optional(obj: object, name: str) -> bool:
    method = getattr(obj, name, None)
    if method is None:
        return False
    is_fixture = getfixturemarker(method) is not None
    if is_fixture:
        return False
    if not callable(method):
        return False
    # If there are any problems allow the exception to raise rather than
    # silently ignoring it.
    method()
    return True