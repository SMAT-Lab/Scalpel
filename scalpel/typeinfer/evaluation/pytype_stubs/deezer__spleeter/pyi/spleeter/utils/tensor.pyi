# (generated with --quick)

from typing import Any, Callable, Dict

__author__: str
__email__: str
__license__: str
pd: module
tf: Any

def check_tensor_shape(tensor_tf, target_shape) -> bool: ...
def dataset_from_csv(csv_path: str, **kwargs) -> Any: ...
def from_float32_to_uint8(tensor, tensor_key: str = ..., min_key: str = ..., max_key: str = ...) -> Any: ...
def from_uint8_to_float32(tensor, tensor_min, tensor_max) -> Any: ...
def pad_and_partition(tensor, segment_len: int) -> Any: ...
def pad_and_reshape(instr_spec, frame_length, F) -> Any: ...
def set_tensor_shape(tensor, tensor_shape) -> Any: ...
def sync_apply(tensor_dict, func: Callable, concat_axis: int = ...) -> Dict[str, Any]: ...
