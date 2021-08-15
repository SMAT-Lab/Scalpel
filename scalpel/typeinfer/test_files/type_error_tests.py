"""
Tomas Bolger 2021
Python 3.8
Test cases for Type Inference module
"""

from contextlib import contextmanager
from collections import defaultdict
from typing import Any, TypeVar
from typing import Dict
import collections
import os
import re

_T = TypeVar('_T')


def add_values(value1, value2) -> Any:
    sum = value1 + value2
    return sum


def append_to_string(str_to_append) -> str:
    my_str = "hello"
    my_str += str_to_append
    return my_str


def get_element(element_index, element_list) -> Any:
    return element_list[element_index]


def create_dict_with_keys(key_list) -> Dict[Any, None]:
    return_dict = {}
    for key in key_list:
        return_dict[key] = None
    return return_dict


def create_default_dict() -> defaultdict:
    my_dict = defaultdict()
    return my_dict


def get_working_directory() -> str:
    return os.getcwd()


def reverse_list(list_to_reverse) -> list:
    reversed_list = []
    for item in list_to_reverse[::-1]:
        reversed_list.append(item)
    return reversed_list


@contextmanager
def ignored(exception):
    try:
        yield
    except exception as e:
        print(str(e))


if __name__ == '__main__':
    a = get_element("hello", {"hello": "world"})
    b = get_element(1, [1, 2, 3, 4])
    with ignored(TypeError):
        # Adding a str and int
        x = add_values("hello", 5)

    with ignored(TypeError):
        # str as index
        y = get_element("2", ["this", "is", "a", "test", "list"])

    with ignored(TypeError):
        # iterate an integer
        z = reverse_list(123456)
