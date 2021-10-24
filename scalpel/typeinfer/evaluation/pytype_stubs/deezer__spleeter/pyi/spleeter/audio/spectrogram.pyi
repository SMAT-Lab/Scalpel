# (generated with --quick)

from typing import Any

__author__: str
__email__: str
__license__: str
hann_window: Any
np: module
stft: Any
tf: Any

def compute_spectrogram_tf(waveform, frame_length: int = ..., frame_step: int = ..., spec_exponent: float = ..., window_exponent: float = ...) -> Any: ...
def pitch_shift(spectrogram, semitone_shift: float = ..., method = ...) -> Any: ...
def random_pitch_shift(spectrogram, shift_min: float = ..., shift_max: float = ..., **kwargs) -> Any: ...
def random_time_stretch(spectrogram, factor_min: float = ..., factor_max: float = ..., **kwargs) -> Any: ...
def time_stretch(spectrogram, factor: float = ..., method = ...) -> Any: ...
