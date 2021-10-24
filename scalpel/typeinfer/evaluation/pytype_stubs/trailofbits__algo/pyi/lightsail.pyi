# (generated with --quick)

import __future__
from typing import Any, Dict, List, Tuple, Type, Union

ANSIBLE_METADATA: Dict[str, Union[str, List[str]]]
AnsibleModule: Any
DOCUMENTATION: str
EXAMPLES: str
HAS_BOTO3: Any
HAS_BOTOCORE: bool
RETURN: str
__metaclass__: Type[type]
absolute_import: __future__._Feature
boto3: Any
boto3_conn: Any
botocore: Any
camel_dict_to_snake_dict: Any
division: __future__._Feature
ec2_argument_spec: Any
get_aws_connection_info: Any
print_function: __future__._Feature
time: module
traceback: module

def _find_instance_info(client, instance_name) -> Any: ...
def core(module) -> None: ...
def create_instance(module, client, instance_name) -> Tuple[bool, Any]: ...
def delete_instance(module, client, instance_name) -> Tuple[bool, Any]: ...
def main() -> None: ...
def restart_instance(module, client, instance_name) -> Tuple[bool, Any]: ...
def startstop_instance(module, client, instance_name, state) -> Tuple[bool, Any]: ...
