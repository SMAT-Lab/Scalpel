# (generated with --quick)

from typing import Any, Dict, List, TextIO, Tuple, TypeVar, Union

HOSTED_NOTEBOOK_INSTRUCTIONS: str
STATEMENT_PREFIXES: List[str]
current_example: int
current_section_name: str
e: Any
example_details: Dict[str, nothing]
examples: List[nothing]
f: TextIO
fpath: str
json: module
line: str
lines: listiterator[str]
os: module
post_stuff: List[nothing]
pprint: module
pre_examples_phase: bool
pre_stuff: List[str]
read_only: Any
result: List[Dict[str, nothing]]
section_text: List[str]
sequence_num: int
title_line: str

_T0 = TypeVar('_T0')
_T1 = TypeVar('_T1')

def convert_to_cells(cell_contents, read_only) -> List[Dict[str, Any]]: ...
def convert_to_notebook(pre_examples_content, parsed_json, post_examples_content) -> None: ...
def generate_code_block(statements: _T0, output: _T1) -> Dict[str, Union[int, str, _T0, _T1]]: ...
def generate_markdown_block(lines: _T0) -> Dict[str, Union[int, str, _T0]]: ...
def inspect_and_sanitize_code_lines(lines) -> Tuple[bool, list]: ...
def is_interactive_statement(line) -> bool: ...
def parse_example_parts(lines, title, current_line) -> Tuple[Any, Dict[str, List[Dict[str, Union[int, list, str]]]]]: ...
def remove_from_beginning(tokens, line) -> Any: ...
