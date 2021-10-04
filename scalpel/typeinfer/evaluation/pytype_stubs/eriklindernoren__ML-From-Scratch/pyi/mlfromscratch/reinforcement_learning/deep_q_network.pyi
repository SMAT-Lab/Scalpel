# (generated with --quick)

import __future__
import collections
from typing import Any, List, Tuple, Type

deque: Type[collections.deque]
division: __future__._Feature
gym: Any
np: module
print_function: __future__._Feature
random: module

class DeepQNetwork:
    __doc__: str
    decay_rate: Any
    env: Any
    epsilon: Any
    gamma: Any
    memory: List[Tuple[Any, Any, Any, Any, Any]]
    memory_size: int
    min_epsilon: Any
    model: Any
    n_actions: Any
    n_states: Any
    def __init__(self, env_name = ..., epsilon = ..., gamma = ..., decay_rate = ..., min_epsilon = ...) -> None: ...
    def _construct_training_set(self, replay) -> Tuple[Any, Any]: ...
    def _memorize(self, state, action, reward, new_state, done) -> None: ...
    def _select_action(self, state) -> Any: ...
    def play(self, n_epochs) -> None: ...
    def set_model(self, model) -> None: ...
    def train(self, n_epochs = ..., batch_size = ...) -> None: ...
