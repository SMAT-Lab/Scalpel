from enum import Enum


class Stmt:
    content = ""
    line_number = -1

    def __init__(self):
        None

    def get_declared_method(self):
        return {}

    def get_content(self):
        return self.content

    def get_line_number(self):
        return self.line_number