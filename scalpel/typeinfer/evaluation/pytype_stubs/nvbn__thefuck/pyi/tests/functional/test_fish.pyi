# (generated with --quick)

from typing import Any, Tuple

containers: Tuple[Tuple[str, str, str], Tuple[str, str, str]]
proc: Any
pytest: Any
test_refuse_with_confirmation: Any
test_select_command_with_arrows: Any
test_with_confirmation: Any
test_without_confirmation: Any

def refuse_with_confirmation(proc, TIMEOUT) -> None: ...
def select_command_with_arrows(proc, TIMEOUT) -> None: ...
def with_confirmation(proc, TIMEOUT) -> None: ...
def without_confirmation(proc, TIMEOUT) -> None: ...
