# (generated with --quick)

import __future__
from typing import Any, Callable, Tuple

FLAGS: Any
absolute_import: __future__._Feature
division: __future__._Feature
flags: Any
hub: Any
optimization: Any
os: module
print_function: __future__._Feature
run_classifier: Any
tf: Any
tokenization: Any

def create_model(is_training, input_ids, input_mask, segment_ids, labels, num_labels, bert_hub_module_handle) -> Tuple[Any, Any, Any, Any]: ...
def create_tokenizer_from_hub_module(bert_hub_module_handle) -> Any: ...
def main(_) -> None: ...
def model_fn_builder(num_labels, learning_rate, num_train_steps, num_warmup_steps, use_tpu, bert_hub_module_handle) -> Callable[[Any, Any, Any, Any], Any]: ...
