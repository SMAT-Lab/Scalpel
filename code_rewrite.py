import os
import sys
import ast
import configparser
import astor
import astunparse
from scalpel.rewriter import Rewriter


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

def main():
    config_data = read_template()
    src_file = sys.argv[1]
    src = open(src_file).read()
    print(src)
    pattern = lambda x:isinstance(x, ast.Assign)
    new_stmt = []
    rewriter = Rewriter(src, config_data, new_stmt)
    #new_ast = rewriter.insert_before()
    new_ast = rewriter.rewrite()
    #new_ast = rewriter.remove()
    #new_ast = rewriter.replace()

    new_src = astor.to_source(new_ast)
    print(new_src)
    return 0

if __name__ == "__main__":
    main()
