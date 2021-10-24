# (generated with --quick)

import enum
from typing import Type

Enum: Type[enum.Enum]
auto: Type[enum.auto]

class Expect(enum.Enum):
    BODY: enum.auto
    REQUEST_HEADERS: enum.auto
    RESPONSE_HEADERS: enum.auto
    SEPARATOR: enum.auto
    __doc__: str

class ExpectSequence:
    RAW_BODY: list
    RAW_EXCHANGE: list
    RAW_REQUEST: list
    RAW_RESPONSE: list
    TERMINAL_BODY: list
    TERMINAL_EXCHANGE: list
    TERMINAL_REQUEST: list
    TERMINAL_RESPONSE: list
    __doc__: str
