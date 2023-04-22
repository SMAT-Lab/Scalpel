"""
FileSystem module for Scalpel. The original import graph will be removed while the similar functionalities are implemented in this module. 
The purpose of this componement is to support modelling large Python project structure in a simplified way. 
This component is still under development.

Author: Jiawei Wang
"""

import os
from dataclasses import dataclass
import ast

from scalpel.core.source_visitor import SourceVisitor


@dataclass
class Node:
    # a data structure that contain information for a module node 
    def __init__(self, name):
        self.name:str = name
        self.full_name:str = ""
        self.children:list = []
        self.parent:str = None
        self.cargo:dict = {}
        self.source:str = ''
        self.ast = None
        self.static_assignments = None
        self.call_links = None
        self.imports = {}
        self.abs_path = None 

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()


class FileSystem:
    """
    This class is an upgraded implementation of import graph which will be removed in to later releases. 
    It is a data structure that allows users to manipulate different files under a Python project. 
    It leverage import relations in each of source files along with their absolute import name. 
    """

    def __init__(self, entry_point, file_ext=".py"):
        """
        To constuct a the filesystem.
        Args:
        entry_point: the top level folder path such as "my-python-projects/homework1". The argument must not endswith slash!
        """
        # entry_point is the top level module folder 
        self.entry_point = entry_point
        # note that the entry_point must not ends with slash. The recommended one is "a/b/c.py"
       # self.root = Node(os.path.basename(self.entry_point))
      
        self.file_ext = file_ext  # can be used to parse pyi files in the future 
    
    
    def _build_dir_tree(self, node):
        if os.path.isdir(node.name) is True:
            os.chdir(node.name)
            
            items = os.listdir('.')
            for item in items:
                child_node = Tree(item)
                child_node.parent = node
                self._build_dir_tree(child_node)
                node.children.append(child_node)
            os.chdir('..')
        else:
            if node.name.endswith(self.file_ext):
            
                with open(node.name, 'r') as f:     
                    try:  
                        source = f.read()
                          
                    except:
                        source = ""

                    node.source = source      
                    try:
                        node.ast = ast.parse(source)
                    except:
                        node.ast = None 
                        
                    #node.class_pair = pair
                    node.prefix = self.leaf2root(node)
                    node.full_name = node.prefix # + '.' + node.name

    def build_dir_tree(self):
        """
        To build enhanced directory tree for further analysis
        """
        cwd = os.getcwd()
        working_dir = os.path.dirname(self.entry_point)
        os.chdir(working_dir)
        self._build_dir_tree(self.root)
        os.chdir(cwd)
    

    def get_leaf_nodes(self) -> list[Node]:
        """
        To return all the leaf nodes in this tree. Each of leaf nodes represents a single Python script.
        During the transversal, full path names to the top level module for each leaf node are generated.
        We will support the intermediate subfolders next.
 
        Returns:  a list of Nodes  
        """

        all_leaf_nodes = []
        for root, dirs, files in os.walk(self.entry_point):
            files = [
                f for f in files if not f[0] == "."
            ]  # skip hidden files such as git files
            dirs[:] = [d for d in dirs if not d[0] == "."]
            for f in files:
                if f.endswith(self.file_ext):    
                    abs_path = os.path.join(root, f)
                    mod_node = Node(f)
                    mod_node.abs_path = abs_path
                    all_leaf_nodes.append(mod_node)


    def format_all_imports(self, import_statement):
        '''
        TODO:
        To convert all import path such as from ..X import fun as  its abs import path.
        
        '''
        pass 
        
       
        
    def go_to_that_node(self, cur_node, visit_path):
        """
        To locate a particular node from the tree from the current node given a visit path from import statement. 
        For instance,  a visit path of [example, module_a, func] means, if we can locate the function definition `func` from module_a under example folder. 
        The function tries to locate the given path using both relative and absolute import path. 
        Args:
        visit_path: a list of names that represent different level python modules.
        """
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
        """
        To parse import statements from the AST tree
        Args:
        tree: Python AST object
        Returns: an import map data structure
        """
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
        """
        To parse import statements from the AST tree
        Args:
        source: source code text
        Returns: class/function definitions, ast tree and alias pairs 
        """
        tree = ast.parse(source, mode='exec')
        visitor = SourceVisitor()
        visitor.visit(tree)
     
        return visitor.result, tree, visitor.pair
    
   

    @staticmethod
    def find_child_by_name(node, name):
        """
        To locate a child node using node name
        """
        for ch in node.children:
            if ch.name == name:
                return ch
        return None

    @staticmethod
    def find_node_by_name(nodes, name):
        """
        To locate a  node using node name
        """
        for node in nodes:
            if node.name == name or node.name.rstrip('.py') == name:
                return node
        return None

