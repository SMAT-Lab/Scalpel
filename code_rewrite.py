import os
import sys
import ast
import configparser
import astor
import astunparse
from scalpel.rewriter import Rewriter
from scalpel.core.util import StmtWalker


def read_template():
    filename = "template"
    config = configparser.ConfigParser(delimiters=('=', ':', '->'))
    config.read(filename)
    config_data = {"Name": {}, "Call":{}, "Stmt":{}}
    for entry in config["Name"]:
        config_data["Name"][entry]= config["Name"][entry]
    for entry in config["Call"]:
        config_data["Call"][entry]= config["Call"][entry]
    for entry in config["Stmt"]:
        config_data["Stmt"][entry]= config["Stmt"][entry]

    return config_data

def Visit_Generator():
    # if this is a module then go to its body
    # if this is  if  then go to tis body
    # recursively 
    pass

def process_template():
    config_data = read_template()
    src_file = sys.argv[1]
    src = open(src_file).read()
    print(src)
    pattern = lambda x:isinstance(x, ast.Assign)
    new_stmt = []
    rewriter = Rewriter(src, config_data, new_stmt)
    new_ast = rewriter.rewrite()
    new_src = astor.to_source(new_ast)
    print(new_src)
    return 0

def main():
    config_data = read_template()
    src_file = sys.argv[1]
    src = open(src_file).read()
    m_ast = ast.parse(src)
    call_node = ast.Call(ast.Name(id='print',ctx=ast.Load()),
                [ast.Constant("testing", None)], [])
    new_stmt = ast.Expr(call_node)
    for node in StmtWalker(m_ast):
        node.insert_after(new_stmt)
        pass

    new_ast = ast.fix_missing_locations(m_ast)
    new_src = astor.to_source(new_ast)
    print(new_src)
    return 0

if __name__ == "__main__":
    main()
