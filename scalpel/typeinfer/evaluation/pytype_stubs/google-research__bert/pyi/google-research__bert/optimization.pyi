# (generated with --quick)

import __future__
from typing import Any, TypeVar, Union

absolute_import: __future__._Feature
division: __future__._Feature
print_function: __future__._Feature
re: module
tf: Any

_T0 = TypeVar('_T0')

class AdamWeightDecayOptimizer(Any):
    __doc__: str
    beta_1: Any
    beta_2: Any
    epsilon: Any
    exclude_from_weight_decay: Any
    learning_rate: Any
    weight_decay_rate: Any
    def __init__(self, learning_rate, weight_decay_rate = ..., beta_1 = ..., beta_2 = ..., epsilon = ..., exclude_from_weight_decay = ..., name = ...) -> None: ...
    def _do_use_weight_decay(self, param_name) -> bool: ...
    def _get_variable_name(self, param_name: _T0) -> Union[str, _T0]: ...
    def apply_gradients(self, grads_and_vars, global_step = ..., name = ...) -> Any: ...

def create_optimizer(loss, init_lr, num_train_steps, num_warmup_steps, use_tpu) -> Any: ...
