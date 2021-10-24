# (generated with --quick)

from typing import Any, List
import unittest.case

QueryNotify: Any
QueryResult: Any
QueryStatus: Any
SitesInformation: Any
os: module
sherlock: module
unittest: module
warnings: module

class SherlockBaseTest(unittest.case.TestCase):
    excluded_sites: List[str]
    query_notify: Any
    site_data_all: dict
    skip_error_sites: bool
    timeout: None
    tor: bool
    unique_tor: bool
    def coverage_total_check(self) -> None: ...
    def detect_type_check(self, detect_type, exist_check = ...) -> None: ...
    def setUp(self) -> None: ...
    def site_data_filter(self, site_list) -> dict: ...
    def username_check(self, username_list, site_list, exist_check = ...) -> None: ...
