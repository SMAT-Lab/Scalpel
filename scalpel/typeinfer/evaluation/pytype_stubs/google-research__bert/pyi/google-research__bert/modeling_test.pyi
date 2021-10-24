# (generated with --quick)

import __future__
from typing import Any, TypeVar

absolute_import: __future__._Feature
collections: module
division: __future__._Feature
json: module
modeling: Any
print_function: __future__._Feature
random: module
re: module
six: module
tf: Any

_T0 = TypeVar('_T0')

class BertModelTest(Any):
    BertModelTester: type
    def assert_all_tensors_reachable(self, sess, outputs) -> None: ...
    @classmethod
    def flatten_recursive(cls, item: _T0) -> list: ...
    @classmethod
    def get_unreachable_ops(cls, graph, outputs) -> list: ...
    @classmethod
    def ids_tensor(cls, shape, vocab_size, rng = ..., name = ...) -> Any: ...
    def run_tester(self, tester) -> None: ...
    def test_config_to_json_string(self) -> None: ...
    def test_default(self) -> None: ...
