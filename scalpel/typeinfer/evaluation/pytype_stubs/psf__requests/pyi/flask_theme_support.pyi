# (generated with --quick)

import pygments.style
import pygments.token
from typing import Dict, Type

Comment: pygments.token._TokenType
Error: pygments.token._TokenType
Generic: pygments.token._TokenType
Keyword: pygments.token._TokenType
Literal: pygments.token._TokenType
Name: pygments.token._TokenType
Number: pygments.token._TokenType
Operator: pygments.token._TokenType
Other: pygments.token._TokenType
Punctuation: pygments.token._TokenType
String: pygments.token._TokenType
Style: Type[pygments.style.Style]
Whitespace: pygments.token._TokenType

class FlaskyStyle(pygments.style.Style):
    background_color: str
    default_style: str
    styles: Dict[pygments.token._TokenType, str]
