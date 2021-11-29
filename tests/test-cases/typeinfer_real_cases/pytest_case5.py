'''
From pytest_saferepr.py
'''
from typing import Any
from typing import Dict
from typing import IO

def _format(
        self,
        object: object,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: Dict[int, Any],
        level: int,
) -> None:
    # Type ignored because _dispatch is private.
    p = self._dispatch.get(type(object).__repr__, None)  # type: ignore[attr-defined]

    objid = id(object)
    if objid in context or p is None:
        # Type ignored because _format is private.
        super()._format(  # type: ignore[misc]
            object,
            stream,
            indent,
            allowance,
            context,
            level,
        )
        return

    context[objid] = 1
    p(self, object, stream, indent, allowance, context, level + 1)
    del context[objid]