# (generated with --quick)

import colorama.ansi
from typing import Any, Dict

Back: colorama.ansi.AnsiBack
Fore: colorama.ansi.AnsiFore
PALETTES: Dict[int, Dict[int, Any]]
Style: colorama.ansi.AnsiStyle
colored: Any
re: module

def _back_color(code) -> str: ...
def _reverse_palette(code) -> Dict[int, str]: ...
def colorize_internal(text, palette_number = ...) -> str: ...
def colorize_internal_firstpage_v1(answer) -> str: ...
