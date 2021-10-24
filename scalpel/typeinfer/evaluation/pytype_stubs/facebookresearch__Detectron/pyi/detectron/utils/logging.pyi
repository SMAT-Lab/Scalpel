# (generated with --quick)

import __future__
import collections
import email.mime.text
from typing import Any, Type

MIMEText: Type[email.mime.text.MIMEText]
absolute_import: __future__._Feature
deque: Type[collections.deque]
division: __future__._Feature
json: module
logging: module
np: module
print_function: __future__._Feature
smtplib: module
sys: module
unicode_literals: __future__._Feature

class SmoothedValue:
    __doc__: str
    count: int
    deque: collections.deque
    series: list
    total: Any
    def AddValue(self, value) -> None: ...
    def GetAverageValue(self) -> Any: ...
    def GetGlobalAverageValue(self) -> Any: ...
    def GetMedianValue(self) -> Any: ...
    def __init__(self, window_size) -> None: ...

def log_json_stats(stats, sort_keys = ...) -> None: ...
def send_email(subject, body, to) -> None: ...
def setup_logging(name) -> logging.Logger: ...
