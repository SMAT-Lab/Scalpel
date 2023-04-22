import ast
import builtins
import math
import operator
import os


# scan a folder recurisively and return all files ending with the flag
def get_path_by_ext(root_dir, flag=".py"):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        files = [
            f for f in files if not f[0] == "."
        ]  # skip hidden files such as git files
        dirs[:] = [d for d in dirs if not d[0] == "."]
        for f in files:
            if f.endswith(flag):
                paths.append(os.path.join(root, f))
    return paths


MATH_FUNCTIONS = [x for x in dir(math) if not "__" in x]
BUILT_IN_FUNCTIONS = [x for x in dir(builtins) if not "__" in x]

ops = {
    # binary
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    # ast.Call: checkfun, # check all built-in functions #APSV: Not implemented? commenting
    ast.BinOp: ast.BinOp,
    #  unary
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.UnaryOp: ast.UnaryOp,
    ast.Not: operator.__not__,
}


def ast_node_eval(node):
    """ "
    This is an implementation of expression node evaluation. The function serves as an alternative to ast.literal_eval()
    """
    ##TODO
    pass
