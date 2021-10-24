# (generated with --quick)

import enum
from typing import Type

Enum: Type[enum.Enum]
__author__: str
__email__: str
__license__: str

class Codec(str, enum.Enum):
    FLAC: str
    M4A: str
    MP3: str
    OGG: str
    WAV: str
    WMA: str
    __doc__: str

class STFTBackend(str, enum.Enum):
    AUTO: str
    LIBROSA: str
    TENSORFLOW: str
    __doc__: str
    @classmethod
    def resolve(cls: type, backend: str) -> str: ...
