from .stmt import Stmt


class AssignStmt(Stmt):
    def __init__(self):
        None

    def get_left_variables(self):
        return None

    # Expression
    def get_right_variables(self):
        return None