# (generated with --quick)

import __future__
from typing import Any, Optional, Type

AnsibleModule: Any
HAS_LINODE_DEPENDENCY: bool
LINODE_IMP_ERR: Optional[str]
LinodeClient: Any
StackScript: Any
__metaclass__: Type[type]
absolute_import: __future__._Feature
division: __future__._Feature
env_fallback: Any
get_user_agent: Any
missing_required_lib: Any
print_function: __future__._Feature
traceback: module

def build_client(module) -> Any: ...
def create_stackscript(module, client, **kwargs) -> Any: ...
def initialise_module() -> Any: ...
def main() -> None: ...
def stackscript_available(module, client) -> Any: ...
