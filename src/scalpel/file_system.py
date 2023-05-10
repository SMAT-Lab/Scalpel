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
    def __init__(self, name, abs_path, mod_src, mod_ast, parent = None,  node_type="module"):
        self.name:str = name   # module name 
        self.abs_path = abs_path
        self.mod_src = mod_src
        self.mod_ast = mod_ast
        self.node_type =  node_type  #   there are two different node:  module and package
        self.parent = parent
        
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
        entry_point: the top level folder (packaage) path such as "my-python-projects/homework1". 
        file_ext: the file extension type of building this class. It is intended to be either Python source files or stub files. 
        """
        # entry_point is the top level module folder 
        self.entry_point = entry_point  
        self.file_ext = file_ext  # can be used to parse pyi files in the future 
        self.all_mod_nodes:List[Node] = []

        assert (self.file_ext in [".py", ".pyi"])  # the guard the inputs
    
    
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
            mod_node = Node(mod_name, abs_path, mod_src, mod_ast, node_type="module")
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
                        self.parse_import(mod_ast)
                        mod_node = Node(mod_name, abs_path, mod_src, mod_ast, parent=root, node_type="module")
                        self.all_mod_nodes.append(mod_node)
                #return 0

                for d in dirs:
                    abs_path = os.path.join(root, d)
                    mod_name = d 
                    mod_src = None
                    mod_ast = None 
                    mod_node = Node(mod_name,abs_path, mod_src, mod_ast, parent=root, node_type="package")
                    self.all_mod_nodes.append(mod_node)
                    

    def get_leaf_nodes(self) -> List[Node]:
        """
        To return all the leaf nodes in this tree. Each of leaf nodes represents a single Python script.
        During the transversal, full path names to the top level module for each leaf node are generated.
        We will support the intermediate subfolders next.
 
        Returns:  a list of Nodes  
        """

        return [node for node in self.all_mod_nodes if node.node_type == "module"]
    
    def get_subpackages(self) -> List[Node]:
        return [node for node in self.all_mod_nodes if node.node_type == "package"]
    
    
    def _meta_data():
        """
        To parse each of modules and extract meta information.
        """
        pass 
   
    
    def format_import_path(self, import_stmt, abs_path):
        abs_import_path = []
        if isinstance(import_stmt, ast.Import):
            for alias in import_stmt.names:
                abs_import_path.append(alias.name)
            pass 
        elif isinstance(import_stmt, ast.ImportFrom):
            import_path_parts = abs_path.split(".")
            abs_import_path + [import_path_parts[:-import_stmt.level] + "." + import_stmt.module]
            pass 
        else:
            raise ("unknown input argument")
    
   
    def parse_import(self, tree)->dict:
        """
        To parse import statements from the AST tree
        Args:
        tree: Python import statement
        Returns: mport path
        """
        module_item_dict = {}
        try:
            for node in ast.walk(tree):
                if isinstance(node, (ast.ImportFrom, ast.Import)):
                    self.format_import_path(node)
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
    ep  = sys.argv[1]  # entry point 
    fs = FileSystem(ep)

    fs.build_dir_tree()
    all_leaf_node = fs.get_leaf_nodes()
    all_package_node = fs.get_subpackages()


    print(len(all_leaf_node), len(all_package_node))
if __name__ == "__main__":
    main()