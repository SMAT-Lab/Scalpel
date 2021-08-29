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
import gzip
import os
import re

_T = TypeVar('_T')


class HelloWorld:
    def __init__(self, num: int):
        self.num = num

    def add(self, other_num: int):
        return self.num + other_num

    def multiply(self, other_num: int):
        return self.num * other_num


class AnotherClass(HelloWorld):

    def __init__(self, num: int):
        super().__init__(num)

    def subtract(self, other_num: int):
        return self.num - other_num


def add_values(value1, value2) -> Any:
    sum = value1 + value2
    return sum


def append_to_string(str_to_append) -> str:
    my_str = "True"
    my_str += str_to_append
    return my_str


def get_element(element_index, element_list) -> Any:
    return element_list[element_index]


def create_dict_with_keys(key_list):
    return_dict = {"hello": 1,
                   "he": "Asd"}
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

def double_return():
    return 5, 10

def function_return_plus_number():
    return 5 + 10 + 100

@contextmanager
def ignored(exception):
    try:
        yield
    except exception as e:
        print(str(e))


def compress(file):
    return gzip.compress(file)

if __name__ == '__main__':
    a = get_element("hello", {"hello": "world"})
    b = get_element(1, [1, 2, 3, 4])

    with ignored(TypeError):
        # Adding a str and int
        x = add_values("hello", "")

    with ignored(TypeError):
        # str as index
        y = get_element(1, ["this", "is", "a", "test", "list"])

    with ignored(TypeError):
        # iterate an integer
        z = reverse_list([123456])

    compress("hello")