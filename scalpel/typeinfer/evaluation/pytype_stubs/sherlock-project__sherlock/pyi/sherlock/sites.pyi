# (generated with --quick)

from typing import Any, Dict, Generator

json: module
operator: module
os: module
requests: module
sys: module

class SiteInformation:
    information: Any
    name: Any
    url_home: Any
    url_username_format: Any
    username_claimed: Any
    username_unclaimed: Any
    def __init__(self, name, url_home, url_username_format, username_claimed, username_unclaimed, information) -> None: ...
    def __str__(self) -> str: ...

class SitesInformation:
    sites: Dict[Any, SiteInformation]
    def __init__(self, data_file_path = ...) -> None: ...
    def __iter__(self) -> Generator[SiteInformation, Any, None]: ...
    def __len__(self) -> int: ...
    def site_name_list(self) -> list: ...
