import ast
import os
import re
import sys
import json
from queue import Queue
from copy import deepcopy
from core import *
#
# TODO
# recursively look for import modules 
# to take transitivaity into account

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
        self.node_type_dict = None
        self.node_type_gt = None
        self.call_links = None 
    def __str__(self):
        return str(self.name)


class ImportGraph:
    # entry point
    def __init__(self, ep, root):
        self.ep = ep
        self.root = root

    def build_dir_tree(self, node):
        if node.name in ['test', 'tests', 'testing']:
            return
        if os.path.isdir(node.name) is True:
            os.chdir(node.name)
            items  = os.listdir('.')
            for item in items:
                child_node = Tree(item)
                child_node.parent =  node
                self.build_dir_tree(child_node)
                node.children.append(child_node)
            os.chdir('..')
        else:
            # this is a file
            if node.name.endswith('.py'):
                source = open(node.name, 'rb').read()
                node.source = source.decode("utf-8", errors="ignore")
                res, tree, pair = self.extract_class_from_source(node.source)
                node.cargo = res
                node.ast = tree
                node.class_pair = pair 
                node.prefix = self.leaf2root(node)
                node.full_name = node.prefix+'.'+node.name

    def parse_import(self, tree):
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

    def extract_class_from_source(self, source):
        try:
            tree = ast.parse(source, mode='exec')
            visitor = SourceVisitor()
            visitor.visit(tree)
            return visitor.result, tree, visitor.pair
        except Exception as e:  # to avoid non-python code
            # non-python code to handle here
            return {}, None, None # return empty 


    def leaf2root(self, node):
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
            path_name = ".".join(reversed(path_to_root[1:]))
            path_name = "{}.{}".format(path_name, node.name.split('.')[0])
            return path_name

    def find_child_by_name(self, node, name):
        for ch in node.children:
            if ch.name == name:
                return ch
        return None

    def find_node_by_name(self, nodes, name):
        for node in nodes:
            if node.name == name or node.name.rstrip('.py')== name:
                return node
        return None

    def go_to_that_node(self,  cur_node, visit_path):
        # current_node 
        # visit_path
        route_length = len(visit_path)
        tmp_node = None
        if route_length == 0:
            return self.root
            #return tmp_node

        # go to the siblings of the current node
        # this is the topmost node
        if cur_node.parent is None:
            return tmp_node


        tmp_node =  self.find_node_by_name(cur_node.parent.children, visit_path[0])
        if tmp_node is not None:
            for i in range(1,route_length):
                tmp_node =  self.find_node_by_name(tmp_node.children, visit_path[i])
                if tmp_node is None:
                    break
        # from the topmost, this rule for Pandas or django  
        elif visit_path[0] == self.root.name:
            tmp_node = self.root
            for i in range(1,route_length):
                tmp_node =  self.find_node_by_name(tmp_node.children, visit_path[i])
                if tmp_node is None:
                    break
            return tmp_node
        # from its parent 
        elif visit_path[0] == cur_node.parent.name:
            tmp_node = cur_node.parent
            for i in range(1,route_length):
                tmp_node =  self.find_node_by_name(tmp_node.children, visit_path[i])
                if tmp_node is None:
                    break
        # we are still in the directory
        if tmp_node is not None and tmp_node.name.endswith('.py') is not True:
           tmp_node =  self.find_node_by_name(tmp_node.children, '__init__.py')

        return tmp_node

    def tree_infer_levels(self, root_node):
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

        # visit all elements from the stack
        for node in leaf_stack:
            # private modules
            if node.name!='__init__.py' and node.name[0]=='_':
                continue
            module_item_dict = parse_import(node.ast)
            if module_item_dict is None:
                continue
            for k, v in module_item_dict.items():
                if k is None or isinstance(k, int):
                    continue
                dst_node = go_to_that_node(root_node, node, k)
                if dst_node  is not None:
                # from  to 
                    all_edges += [(dst_node.full_name, node.full_name)]
        #print(len(all_edges))
        all_edges = list(set(all_edges)) 

        for node in leaf_stack:
            if node.class_pair is not None:
                for ch_class,parent_class in node.class_pair.items():
                    if parent_class is None:
                        continue
                    if parent_class in node.cargo:
                        for k, v in node.cargo[parent_class].items():
                            if k not in node.cargo[ch_class]:  # child class
                                node.cargo[ch_class][k] = v 
            API_prefix = leaf2root(node) 
            #node_API_lst = make_API_full_name(node.cargo, API_prefix)
            #API_name_lst.extend(node_API_lst)

        return API_name_lst

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
        if entry_points is None:
            continue
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
