"""
FileSystem module for Scalpel. The original import graph will be removed while the similar functionalities are implemented in this module. 
The purpose of this componement is to support modelling large Python project structure in a simplified way. 
This component is still under development.

Author: Jiawei Wang
"""

import os
import sys 
import ast
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Node:
    """
    This is the basic unit in the FS. Each node represents a single Python module files.
    Module name, absolute path name, AST and source string are recorded in this dataclass.
    In addition, fields of its parent and childs are recorded. 
    """
    def __init__(self, name, abs_path, mod_src, mod_ast, mode_type="module"):
        self.name:str = name   # module name 
        self.abs_path = abs_path
        self.mod_src = mod_src
        self.mod_ast = mod_ast
        self.mod_type =  mode_type  #   there are two different node:  module and package
        
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
        file_ext: the file extension type. 
        """
        # entry_point is the top level module folder 
        self.entry_point = entry_point  
        self.file_ext = file_ext  # can be used to parse pyi files in the future 
        self.all_mod_nodes:List[Node] = []
    
    
    def build_dir_tree(self):
        """
        To build enhanced directory tree for further analysis
        """
        if os.path.isfile(self.entry_point):
            fn = os.path.basename(self.entry_point)
            abs_path = self.entry_point
            mod_name = fn 
            mod_src = open(abs_path).read()
            mod_ast = ast.parse(mod_src)
            mod_node = Node(mod_name, abs_path, mod_src, mod_ast)
            self.all_mod_nodes.append(mod_node)
        else:
            for root, dirs, files in os.walk(self.entry_point):
                files = [
                    f for f in files if not f[0] == "."
                ]  # skip hidden files such as git files
                dirs[:] = [d for d in dirs if not d[0] == "."]
                for f in files:
                    if f.endswith(self.file_ext):    
                        abs_path = os.path.join(root, f)
                        mod_name = f 
                        mod_src = open(abs_path).read()
                        mod_ast = ast.parse(mod_src)
                        mod_node = Node(mod_name, abs_path, mod_src, mod_ast)
                        self.all_mod_nodes.append(mod_node)
                #return 0
                
                for d in dirs:
                    
                    abs_path = os.path.join(root, d)
                    mod_name = d 
                    mod_src = None
                    mod_ast = None 
                    mod_node = Node(mod_name,abs_path, mod_src, mod_ast)
                    self.all_mod_nodes.append(mod_node)
                    

    def get_leaf_nodes(self) -> List[Node]:
        """
        To return all the leaf nodes in this tree. Each of leaf nodes represents a single Python script.
        During the transversal, full path names to the top level module for each leaf node are generated.
        We will support the intermediate subfolders next.
 
        Returns:  a list of Nodes  
        """

        return self.all_mod_nodes
    
    def format_all_imports(self, import_statement):
        '''
        TODO:
        To convert all import path such as from ..X import fun as  its abs import path.
        
        '''
        pass 
        
    '''

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
        
    '''
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

def main():
    ep  = sys.argv[1]

    fs = FileSystem(ep)

    fs.build_dir_tree()
    all_leaf_node = fs.get_leaf_nodes()


    print(len(all_leaf_node))
if __name__ == "__main__":
    main()