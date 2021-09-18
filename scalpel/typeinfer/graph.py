"""
Tree and import graph for type inference
"""

import os
from scalpel.core.source_visitor import *


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
        self.line_numbers = {}
        self.static_assignments = None
        self.call_links = None

    def __str__(self):
        return str(self.name)


class ImportGraph:

    def __init__(self, entry_point, root):
        self.entry_point = entry_point
        self.root = root

    def build_dir_tree(self, node):
        if os.path.isdir(node.name) is True:
            os.chdir(node.name)
            items = os.listdir('.')
            for item in items:
                child_node = Tree(item)
                child_node.parent = node
                self.build_dir_tree(child_node)
                node.children.append(child_node)
            os.chdir('..')
        else:
            if node.name.endswith('.py'):
                with open(node.name, 'rb') as source_file:
                    source = source_file.read()
                    node.source = source.decode("utf-8", errors="ignore")
                    res, tree, pair = self.extract_class_from_source(node.source)
                    node.cargo = res
                    node.ast = tree
                    node.class_pair = pair
                    node.prefix = self.leaf2root(node)
                    node.full_name = node.prefix + '.' + node.name

    def go_to_that_node(self, cur_node, visit_path):
        route_length = len(visit_path)
        tmp_node = None
        if route_length == 0:
            return self.root

        # Go to the siblings of the current node
        # This is the topmost node
        if cur_node.parent is None:
            return tmp_node

        tmp_node = self.find_node_by_name(cur_node.parent.children, visit_path[0])
        if tmp_node is not None:
            for i in range(1, route_length):
                tmp_node = self.find_node_by_name(tmp_node.children, visit_path[i])
                if tmp_node is None:
                    break
        elif visit_path[0] == self.root.name:
            # From the topmost, this rule for Pandas or django
            tmp_node = self.root
            for i in range(1, route_length):
                tmp_node = self.find_node_by_name(tmp_node.children, visit_path[i])
                if tmp_node is None:
                    break
            return tmp_node
        elif visit_path[0] == cur_node.parent.name:
            # From its parent
            tmp_node = cur_node.parent
            for i in range(1, route_length):
                tmp_node = self.find_node_by_name(tmp_node.children, visit_path[i])
                if tmp_node is None:
                    break
        # we are still in the directory
        if tmp_node is not None and tmp_node.name.endswith('.py') is not True:
            tmp_node = self.find_node_by_name(tmp_node.children, '__init__.py')

        return tmp_node

    @staticmethod
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
        except AttributeError:
            return None

    @staticmethod
    def extract_class_from_source(source):
        try:
            tree = ast.parse(source, mode='exec')
            visitor = SourceVisitor()
            visitor.visit(tree)
            return visitor.result, tree, visitor.pair
        except Exception as e:  # To avoid non-python code
            # Non-python code to handle here
            print(e)
            return {}, None, None  # Return empty

    @staticmethod
    def leaf2root(node):
        tmp_node = node
        path_to_root = []
        # not init.py
        while tmp_node is not None:
            path_to_root.append(tmp_node.name)
            tmp_node = tmp_node.parent
        if node.name == '__init__.py':
            # path_to_root = path_to_root[1:]
            path_name = ".".join(reversed(path_to_root))
            return path_name
        else:
            path_name = ".".join(reversed(path_to_root[1:]))
            path_name = "{}.{}".format(path_name, node.name.split('.')[0])
            return path_name

    @staticmethod
    def find_child_by_name(node, name):
        for ch in node.children:
            if ch.name == name:
                return ch
        return None

    @staticmethod
    def find_node_by_name(nodes, name):
        for node in nodes:
            if node.name == name or node.name.rstrip('.py') == name:
                return node
        return None
