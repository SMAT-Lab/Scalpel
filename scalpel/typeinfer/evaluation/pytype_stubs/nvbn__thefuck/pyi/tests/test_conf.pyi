# (generated with --quick)

import mock
from typing import Any, Type

Mock: Type[mock.Mock]
TestSettingsFromEnv: Any
const: module
load_source: Any
os: module
pytest: Any
six: module
test_get_user_dir_path: Any

class TestInitializeSettingsFile:
    def test_create_if_doesnt_exists(self, settings) -> None: ...
    def test_ignore_if_exists(self, settings) -> None: ...

class TestSettingsFromFile:
    def test_from_file(self, load_source, settings) -> None: ...
    def test_from_file_with_DEFAULT(self, load_source, settings) -> None: ...

def test_settings_defaults(load_source, settings) -> None: ...
def test_settings_from_args(settings) -> None: ...
