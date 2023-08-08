from stmt import Stmt

class InvokeStmt(Stmt):

    def __init__(self):
        None

    def get_invoked_method_name(self):
        """
            return the method name involved in the InvokeStmt
        """
        return ""

    def infer_invoked_method(self):
        """
            Infer the invoked method (full signature)
            If fails, TD
        """
        return None