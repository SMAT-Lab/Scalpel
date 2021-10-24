# (generated with --quick)

import email.header
import email.mime.text
import operator
from typing import Any, Dict, List, Optional, Type, Union

ACCOUNT: Dict[str, str]
API: Dict[str, str]
CONTENT_FORMAT: str
DAY: int
Header: Type[email.header.Header]
MAIL: Dict[str, Union[int, str]]
MIMEText: Type[email.mime.text.MIMEText]
RECEIVERS: List[nothing]
STARS: int
content: List[str]
datetime: module
itemgetter: Type[operator.itemgetter]
logger: logging.Logger
logging: module
os: module
requests: module
smtplib: module

def analyze(json_data) -> list: ...
def check_condition(data) -> Optional[bool]: ...
def get_all_data() -> list: ...
def get_data(page = ...) -> Any: ...
def get_stars(data) -> List[Dict[str, Any]]: ...
def make_content() -> List[str]: ...
def send_email(receivers, email_content) -> None: ...
