import ast
import os
import re
import sys
from queue import Queue
from copy import deepcopy
#from ..core import *
from ..core.func_calls_visitor import get_func_calls

def call_graph_single():
    filename = sys.argv[1]
    source = open(filename, 'r').read()
    tree = ast.parse(source, mode='exec')
    #get_func_def_nodes(tree)

    call_list = {}
    for node in ast.walk(tree):
          if isinstance(node, ast.FunctionDef):
              call_list[node.name] = get_func_calls(node)
    G = nx.Graph()
    G.add_nodes_from(list(call_list.keys()))
    for def_name, call_list in call_list.items():
        call_list_tmp = call_list[1:]
        called_names = [tmp[0] for tmp in call_list_tmp]
        for name in called_names:
            G.add_edge(def_name, name)
    return G
