# (generated with --quick)

import __future__
from typing import Annotated, Any, Dict, List, Optional, Type, Union

ANSIBLE_METADATA: Dict[str, Union[str, List[str]]]
AnsibleModule: Any
DOCUMENTATION: str
DigitalOceanHelper: Any
EXAMPLES: str
RETURN: str
__metaclass__: Type[type]
absolute_import: __future__._Feature
division: __future__._Feature
env_fallback: Any
fetch_url: Any
json: module
print_function: __future__._Feature
time: module

class Response:
    body: Any
    info: Any
    json: Annotated[Any, 'property']
    status_code: Annotated[Any, 'property']
    def __init__(self, resp, info) -> None: ...

def assign_floating_id_to_droplet(module, rest) -> None: ...
def associate_floating_ips(module, rest) -> None: ...
def core(module) -> None: ...
def create_floating_ips(module, rest) -> None: ...
def get_floating_ip_details(module, rest) -> Any: ...
def main() -> None: ...
def wait_action(module, rest, ip, action_id, timeout = ...) -> Optional[bool]: ...
