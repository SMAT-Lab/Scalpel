# (generated with --quick)

from typing import Any, List, Tuple

HEADER: str
PLIST_LOCATION: str
PLIST_TYPES: List[str]
csv: module
glob: module
hashlib: module
os: module
plistlib: module
subprocess: module

def GetComment(plist, comments) -> Any: ...
def GetPlistValue(plist, value) -> Any: ...
def GetProgram(plist) -> Tuple[Any, str]: ...
def HashFile(filename) -> str: ...
def LoadPlist(filename) -> Any: ...
def main() -> None: ...
