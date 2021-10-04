# (generated with --quick)

import __future__
from typing import Any
import uuid

_DETECTRON_S3_BASE_URL: str
absolute_import: __future__._Feature
division: __future__._Feature
errno: module
hashlib: module
logger: logging.Logger
logging: module
os: module
pickle: module
print_function: __future__._Feature
re: module
six: module
sys: module
unicode_literals: __future__._Feature
urllib: module

def _get_file_md5sum(file_name) -> bytes: ...
def _get_reference_md5sum(url) -> Any: ...
def _progress_bar(count, total) -> None: ...
def assert_cache_file_is_ok(url, file_path) -> None: ...
def cache_url(url_or_file, cache_dir) -> Any: ...
def download_url(url, dst_file_path, chunk_size = ..., progress_hook = ...) -> int: ...
def load_object(file_name) -> Any: ...
def save_object(obj, file_name, pickle_format = ...) -> None: ...
def uuid4() -> uuid.UUID: ...
