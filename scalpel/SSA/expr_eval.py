import ast, operator, math
import numpy as np 
import logging

logger = logging.getLogger(__file__)

def _raise_malformed_node(node):
    msg = "malformed node or string"
    if lno := getattr(node, 'lineno', None):
        msg += f' on line {lno}'
    raise ValueError(msg + f': {node!r}')

def _convert_num(node):
    if not isinstance(node, Constant) or type(node.value) not in (int, float, complex):
        _raise_malformed_node(node)
    return node.value
def _convert_signed_num(node):
    if isinstance(node, UnaryOp) and isinstance(node.op, (UAdd, USub)):
        operand = _convert_num(node.operand)
        if isinstance(node.op, UAdd):
            return + operand
        else:
            return - operand
    return _convert_num(node)

def _convert(node):
    if isinstance(node, Constant):
        return node.value
    elif isinstance(node, Tuple):
        return tuple(map(_convert, node.elts))
    elif isinstance(node, List):
        return list(map(_convert, node.elts))
    elif isinstance(node, Set):
        return set(map(_convert, node.elts))
    elif (isinstance(node, Call) and isinstance(node.func, Name) and node.func.id == 'set' and node.args == node.keywords == []):
        return set()
    elif isinstance(node, Dict):
        if len(node.keys) != len(node.values):
            _raise_malformed_node(node)
        return dict(zip(map(_convert, node.keys),
                        map(_convert, node.values)))

    elif isinstance(node, BinOp) and isinstance(node.op, (Add, Sub)):
        left = _convert_signed_num(node.left)
        right = _convert_num(node.right)
        if isinstance(left, (int, float)) and isinstance(right, complex):
            if isinstance(node.op, Add):
                return left + right
            else:
                return left - right
    return _convert_signed_num(node)

def safe_eval(tree):

    def checkmath(x, *args):
        if x not in [x for x in dir(math) if not "__" in x]:
            return None

        fun = getattr(math, x)
        return fun(*args)
    
    def check_numpy(x, *args):
        fun = getattr(np, x)
        #fun = np.array
        return fun(*args)


    binOps = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.Call: checkmath,
        ast.BinOp: ast.BinOp,
    }

    unOps = {
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.UnaryOp: ast.UnaryOp,
        ast.Not: operator.__not__
    }

    ops = tuple(binOps) + tuple(unOps)

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.List):
            return list(map(_eval, node.elts))
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.value
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            if isinstance(node.left, ops):
                left = _eval(node.left)
            else:
                left = _eval(node.left)
            if isinstance(node.right, ops):
                right = _eval(node.right)
            else:
                right = _eval(node.right)
            if left is not None and right is not None:
                return binOps[type(node.op)](left, right)
            return None

        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.operand, ops):
                operand = _eval(node.operand)
            else:
                operand = _eval(node.operand)
            return unOps[type(node.op)](operand)

        elif isinstance(node, ast.Call) and hasattr(node.func, "id"):
            args = [_eval(x) for x in node.args]
            r = checkmath(node.func.id, *args)
            return r
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if hasattr(node.func.value, "id") and node.func.value.id== "np":
                args = [_eval(x) for x in node.args]     
                attr_name = node.func.attr 
                res = check_numpy(attr_name, *args)   
                return res   
            
        else:
            return None
            raise SyntaxError(f"Bad syntax, {type(node)}")

    return _eval(tree)
def type_eval(expr_node):
    result = safe_eval(expr_node)
    return result 
    if result is not None :
        return None
    return type(result).__name__

def src_to_node(src):

    tree = ast.parse(src, mode="eval")
    return tree.body

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    assert type_eval(src_to_node("np.sum([1,2,3,4])")) == 10
    assert type_eval(src_to_node("np.mean([1,2,3,4])")) == 2.5
    
    #print(res, np.array([1,2,3,4]))
     
    assert type_eval(src_to_node("1+1")) == 2
    assert type_eval(src_to_node("1+-5"))== -4
    assert type_eval(src_to_node("-1")) == -1
    assert type_eval(src_to_node("-+1")) == -1
    assert type_eval(src_to_node("(100*10)+6")) == 1006
    assert type_eval(src_to_node("100*(10+6)")) == 1600
    assert type_eval(src_to_node("2**4")) == 2**4
    assert type_eval(src_to_node("sqrt(16)+1")) == math.sqrt(16) + 1
    assert type_eval(src_to_node("1.2345 * 10")) == 1.2345 * 10
    assert type_eval(src_to_node('"a"*10')) == "aaaaaaaaaa"
    assert type_eval(src_to_node('a*10')) == None
    res =  type_eval(src_to_node("[]+[]"))
    res = type_eval(src_to_node('"a"*3'))
    assert type_eval(src_to_node("[]+[]")) == []
    assert type_eval(src_to_node("[1,2,3] + [1,2,3]")) == [1,2,3,1,2,3]
    assert type_eval(src_to_node('"a"*3')) == "aaa" 

