import os
import sys
import ast
import json
from scalpel.core.mnode import MNode

def main():
    filename =sys.argv[1]
    src = open(filename).read()
    mnode = MNode("filename")
    mnode.source = src
    mnode.gen_ast()
    results = mnode.parse_function_body()
    print(json.dumps(results))

if __name__ == '__main__':
    main()
