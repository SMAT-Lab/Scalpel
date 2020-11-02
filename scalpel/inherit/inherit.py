import ast
import os
import re
import sys
import json
from queue import Queue
from copy import deepcopy
from core import *
from wheel_inspect import inspect_wheel
import tarfile
from zipfile import ZipFile
from pkg_resources import parse_version
import networkx as nx

class Tree:
    def __init__(self, name):
        self.name = name
        self.full_name = ""
        self.children = []
        self.parent = None
        self.cargo = {}
        self.source = ''
        self.ast = None
        self.class_pair = None
    def __str__(self):
        return str(self.name)

def parse_import(tree):
    module_item_dict = {}
    try:
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module is None and node.level not in module_item_dict:
                    module_item_dict[node.level] = []
                elif node.module not in module_item_dict:
                   module_item_dict[node.module] = []
                items = [nn.__dict__ for nn in node.names] 
                for d in items:
                    if node.module is None:
                        module_item_dict[node.level].append(d['name'])
                    else:
                        module_item_dict[node.module].append(d['name'])

        return module_item_dict
    except(AttributeError):
        return None
 
def gen_AST(filename):
    try:
        source = open(filename).read()
        tree = ast.parse(source, mode='exec')
        return tree
    except (SyntaxError,UnicodeDecodeError,):  # to avoid non-python code
        pass
        return None
def parse_pyx(filename):
    lines = open(filename).readlines()
    all_func_names = []
    for line in lines:
        names = re.findall('def ([\s\S]*?)\(', str(line))
        if len(names)>0:
            all_func_names.append(names[0])

def extract_class(filename):
    try:
        source = open(filename).read()
        tree = ast.parse(source, mode='exec')
        visitor = SourceVisitor()
        visitor.visit(tree)
        return visitor.result, tree
    except Exception as e:  # to avoid non-python code
        # fail passing python3 
        if filename[-3:] == 'pyx':
            #print(filename)
            parse_pyx(filename)
        return {}, None  # return empty 

def extract_class_from_source(source):
    try:
        tree = ast.parse(source, mode='exec')
        visitor = SourceVisitor()
        visitor.visit(tree)
        return visitor.result, tree, visitor.pair
    except Exception as e:  # to avoid non-python code
        # fail passing python3 
        #if filename[-3:] == 'pyx':
        #    #print(filename)
        #    parse_pyx(filename)
        return {}, None, None # return empty 

def build_dir_tree(node):
    if node.name in ['test', 'tests', 'testing']:
        return 
    if os.path.isdir(node.name) is True:
        os.chdir(node.name)
        items  = os.listdir('.')
        for item in items:
            child_node = Tree(item)
            child_node.parent =  node
            build_dir_tree(child_node)
            node.children.append(child_node)
        os.chdir('..')
    else:
        # this is a file
        if node.name.endswith('.py'):
            source = open(node.name, 'rb').read()
            node.source = source.decode("utf-8", errors="ignore")
            res, tree, pair = extract_class_from_source(node.source)
            node.cargo = res
            node.ast = tree
            node.class_pair = pair 
            node.prefix = leaf2root(node)
            node.full_name = node.prefix+'.'+node.name

def leaf2root(node):
    tmp_node = node
    path_to_root = []
    # not init.py
    while tmp_node is not None:
        path_to_root.append(tmp_node.name)
        tmp_node = tmp_node.parent
    if node.name == '__init__.py':
        #path_to_root = path_to_root[1:]
        path_name = ".".join(reversed(path_to_root))
        return path_name
    else:
        path_name = ".".join(reversed(path_to_root))
        path_name = "{}.{}".format(path_name, node.name.split('.')[0])
        return path_name

def find_child_by_name(node, name):
    for ch in node.children:
        if ch.name == name:
            return ch
    return None

def find_node_by_name(nodes, name):
    for node in nodes:
        if node.name == name or node.name.rstrip('.py')== name:
            return node
    return None

def go_to_that_node(root, cur_node, visit_path):
    route_node_names = visit_path.split('.')
    route_length = len(route_node_names)
    tmp_node = None
    # go to the siblings of the current node
    tmp_node =  find_node_by_name(cur_node.parent.children, route_node_names[0])
    if tmp_node is not None:
        for i in range(1,route_length):
            tmp_node =  find_node_by_name(tmp_node.children, route_node_names[i])
            if tmp_node is None:
                break
    # from the topmost 
    elif route_node_names[0] == root.name:
        tmp_node = root
        for i in range(1,route_length):
            tmp_node =  find_node_by_name(tmp_node.children, route_node_names[i])
            if tmp_node is None:
                break
        return tmp_node
    # from its parent 
    elif route_node_names[0] == cur_node.parent.name:
        tmp_node = cur_node.parent
        for i in range(1,route_length):
            tmp_node =  find_node_by_name(tmp_node.children, route_node_names[i])
            if tmp_node is None:
                break
    # we are still in the directory
    if tmp_node is not None and tmp_node.name.endswith('.py') is not True:
       tmp_node =  find_node_by_name(tmp_node.children, '__init__.py')

    return tmp_node

def tree_infer_levels(root_node):
    API_name_lst = []
    leaf_stack = []
    working_queue = []
    working_queue.append(root_node)
    all_nodes = []
    all_edges = []
    # bfs to search all I leafs

    while len(working_queue)>0:
        tmp_node = working_queue.pop(0)
        if tmp_node.name.endswith('.py') == True:
            leaf_stack.append(tmp_node)
        # to determine the order
        # to do 
        #module_level_graph(root_node, tmp_node)
        working_queue.extend(tmp_node.children)
    #G = nx.DiGraph()
    G = nx.Graph()

    # visit all elements from the stack
    all_edges = []
    for node in leaf_stack:
        if node.class_pair is None:
            continue
        for k, v in node.class_pair.items():
            all_edges += [(v, k)]
            # v is the parent

    all_node_names  = []
    for e in all_edges:
        all_node_names += [e[0]]
        all_node_names += [e[1]]
    all_node_names =  list(set(all_node_names))
    G.add_nodes_from(all_node_names)
    G.add_edges_from(all_edges)
    N_node = G.number_of_nodes()
    N_edge = G.number_of_edges()
    N_cluster = nx.number_connected_components(G)
    #print(N_node, N_edge, N_cluster)
    print( N_cluster)


    return API_name_lst

def search_targets(root_dir, targets):
     entry_points = []
     for root, dirs, files in os.walk(root_dir):
         n_found = 0
         for t in targets:
             if t in dirs :
                entry_points.append(os.path.join(root, t))
                n_found += 1
             elif t+'.py' in files:
                 entry_points.append(os.path.join(root, t+'.py'))
                 n_found += 1
         if n_found == len(targets):
             return entry_points
     return None
# filter wheel
# notice we will add egginfo soon
#def filter_wheel(path):


def process_wheel(path, l_name):
    # there will be multiple wheel files
    res = []
    all_file_names = os.listdir(path)
    whl_final = ''
    max_py_ver = ''
    for fn in all_file_names:
        if fn.endswith('.whl') and (fn.find('linux')>=0 or fn.find('any')>=0):  # this is a wheel
            whl_path = os.path.join(path, fn)
            try:
                output = inspect_wheel(whl_path)
                if output['pyver'][-1]> max_py_ver:  # -1 means the last one. Use the biggest version number
                    max_py_ver = output['pyver'][-1]
                    whl_final = fn
            except Exception as e:
                print("failed to handle {}".format(whl_path))
                print(e)
    if whl_final != '':
        whl_path = os.path.join(path, whl_final)
        output = inspect_wheel(whl_path)
        #print(output.keys())
        if 'top_level' not in output['dist_info']:
            top_levels = [l_name]
        else:
            top_levels = output['dist_info']['top_level']

        with ZipFile(whl_path, 'r') as zipObj:
           # Extract all the contents of zip file in current directory
           source_dir = os.path.join(path, 'tmp')
           if not os.path.exists(source_dir):
               zipObj.extractall(source_dir)
        entry_points = search_targets(source_dir, top_levels)
        return entry_points
    return None

def process_single_module(module_path):
    API_name_lst = []
    # process other modules !!!
    if os.path.isfile(module_path):
        pass
        #name_segments =  os.path.basename(module_path).rstrip('.py*') # .py and .pyx
        # process a single file module
        #res, tree = extract_class(module_path)
        #node_API_lst = make_API_full_name(res, name_segments)
        #API_name_lst.extend(node_API_lst)
    else:
        first_name = os.path.basename(module_path)
        working_dir = os.path.dirname(module_path)
        path = []
        cwd = os.getcwd() # save current working dir
        os.chdir(working_dir)
        root_node = Tree(first_name)
        build_dir_tree(root_node)
        API_name_lst = tree_infer_levels(root_node)
        os.chdir(cwd) # go back cwd
    return API_name_lst

def process_lib_single():
    l_name = sys.argv[1]
    all_lib_dir = '/data/sdb/jiawei/lib_history'
    API_data = {"module":[], "API":{}, "version":[]}
    lib_dir = os.path.join(all_lib_dir, l_name)
    versions = os.listdir(lib_dir)
    versions.sort(key=lambda x:parse_version(x))
    API_data['version'] = versions
    #for v in versions[-1:]:
    for v in versions:
        v_dir = os.path.join(lib_dir, v)
        entry_points  = process_wheel(v_dir, l_name)
        if entry_points is not None:
            API_data['module'] = entry_points
            for ep in entry_points:
              API_name_lst = process_single_module(ep)  # finish one version 
              if API_name_lst is None:
                  continue
              for name in API_name_lst:
                  # why it is None
                  # matplotlib
                  if name not in API_data['API']:
                      API_data['API'][name] = [v]
                  else:
                      API_data['API'][name] += [v]
    #print(len(API_data['API']))
    # finish all versions for a single one
    f = open("new_data/{}.json".format(l_name), 'w')
    f.write(json.dumps(API_data))
    f.close()


def test_parse_imports():
    filename = sys.argv[1]
    source = open(filename, 'r').read()
    tree = ast.parse(source, mode='exec')
    res = parse_import(tree)
    for k, v in res.items():
        print(k, v)
    return 0
if __name__ == '__main__':
    #main()
    #process_lib()
    process_lib_single()
