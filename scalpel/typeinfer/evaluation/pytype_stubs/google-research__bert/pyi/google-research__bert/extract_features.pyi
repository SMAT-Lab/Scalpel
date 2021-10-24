# (generated with --quick)

import __future__
from typing import Any, Callable, List

FLAGS: Any
absolute_import: __future__._Feature
codecs: module
collections: module
division: __future__._Feature
flags: Any
json: module
modeling: Any
print_function: __future__._Feature
re: module
tf: Any
tokenization: Any

class InputExample:
    text_a: Any
    text_b: Any
    unique_id: Any
    def __init__(self, unique_id, text_a, text_b) -> None: ...

class InputFeatures:
    __doc__: str
    input_ids: Any
    input_mask: Any
    input_type_ids: Any
    tokens: Any
    unique_id: Any
    def __init__(self, unique_id, tokens, input_ids, input_mask, input_type_ids) -> None: ...

def _truncate_seq_pair(tokens_a, tokens_b, max_length) -> None: ...
def convert_examples_to_features(examples, seq_length, tokenizer) -> List[InputFeatures]: ...
def input_fn_builder(features, seq_length) -> Callable[[Any], Any]: ...
def main(_) -> None: ...
def model_fn_builder(bert_config, init_checkpoint, layer_indexes, use_tpu, use_one_hot_embeddings) -> Callable[[Any, Any, Any, Any], Any]: ...
def read_examples(input_file) -> List[InputExample]: ...
