'''
From pytest_outcomes.py
'''
import sys
from typing import Any
from typing import Optional


def importorskip(
    modname: str, minversion: Optional[str] = None, reason: Optional[str] = None
) -> Any:
    """Import and return the requested module ``modname``, or skip the
    current test if the module cannot be imported.

    :param str modname:
        The name of the module to import.
    :param str minversion:
        If given, the imported module's ``__version__`` attribute must be at
        least this minimal version, otherwise the test is still skipped.
    :param str reason:
        If given, this reason is shown as the message when the module cannot
        be imported.

    :returns:
        The imported module. This should be assigned to its canonical name.

    Example::

        docutils = pytest.importorskip("docutils")
    """
    import warnings

    __tracebackhide__ = True
    compile(modname, "", "eval")  # to catch syntaxerrors

    with warnings.catch_warnings():
        # Make sure to ignore ImportWarnings that might happen because
        # of existing directories with the same name we're trying to
        # import but without a __init__.py file.
        warnings.simplefilter("ignore")
        try:
            __import__(modname)
        except ImportError as exc:
            if reason is None:
                reason = f"could not import {modname!r}: {exc}"
            raise Skipped(reason, allow_module_level=True) from None
    mod = sys.modules[modname]
    if minversion is None:
        return mod
    verattr = getattr(mod, "__version__", None)
    if minversion is not None:
        # Imported lazily to improve start-up time.
        from packaging.version import Version

        if verattr is None or Version(verattr) < Version(minversion):
            raise Skipped(
                "module %r has __version__ %r, required is: %r"
                % (modname, verattr, minversion),
                allow_module_level=True,
            )
    return mod