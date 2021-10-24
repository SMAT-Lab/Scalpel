# (generated with --quick)

import argparse
from typing import Any, Dict, Optional, Tuple, Type

ArgumentParser: Type[argparse.ArgumentParser]
FuturesSession: Any
QueryNotifyPrint: Any
QueryResult: Any
QueryStatus: Any
RawDescriptionHelpFormatter: Type[argparse.RawDescriptionHelpFormatter]
SitesInformation: Any
TorRequest: Any
__version__: str
csv: module
module_name: str
os: module
platform: module
re: module
requests: module
sys: module

class SherlockFuturesSession(Any):
    def request(self, method, url, hooks = ..., *args, **kwargs) -> Any: ...

def get_response(request_future, error_type, social_network) -> Tuple[Any, Optional[str], Optional[str]]: ...
def main() -> None: ...
def monotonic() -> float: ...
def sherlock(username, site_data, query_notify, tor = ..., unique_tor = ..., proxy = ..., timeout = ...) -> Dict[Any, Dict[str, Any]]: ...
def timeout_check(value) -> float: ...
