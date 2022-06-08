import ast
from  _ast import *
import pkgutil
import astor
import os
import sys


def iter_fields(node):
    """
    Yield a tuple of ``(fieldname, value)`` for each field in ``node._fields``
    that is present on *node*.
    """
    for field in node._fields:
        try:
            yield field, getattr(node, field)
        except AttributeError:
            pass


def iter_child_nodes(node):
    """
    Yield all direct child nodes of *node*, that is, all fields that are nodes
    and all items of fields that are lists of nodes.
    """
    for name, field in iter_fields(node):
        if isinstance(field, AST):
            yield field
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, AST):
                    yield item


def iter_stmt_children(node):
    """
    Yield all direct child nodes of *node*, that is, all fields that are nodes
    and all items of fields that are lists of nodes.
    """
    children = []
    for name, field in iter_fields(node):
        if isinstance(field, ast.stmt):
            yield field
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, ast.stmt):
                    yield item


def find_local_modules(import_smts):
    smts = "\n".join(import_smts)
    tree = ast.parse(smts, mode='exec')
    search_path = ['.']
    module_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) :
            for nn in node.names:
                module_names.add(nn.name.split('.')[0])
        if isinstance(node, ast.ImportFrom):
            if node.level==2:
                search_path += ['..']
            if node.module is not None:
                module_names.add(node.module.split('.')[0])
            else:
                for nn in node.names:
                    module_names.add(nn.name)
    module_name_plus = ['random', 'unittest', 'warning', 'os', 'pandas', 'IPython', 'seaborn', 'matplotlib', 'sklearn', 'numpy', 'scipy', 'math', 'matplotlib']
    search_path = list(set(search_path))
    all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
    all_modules += list(sys.builtin_module_names) + module_name_plus
    result = []
    for m_name in module_names:
        if m_name not in all_modules:
            result += [m_name]
    return result


def get_path_by_extension(root_dir, num_of_required_paths, flag='.ipynb'):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        files = [f for f in files if not f[0] == '.'] 
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            if file.endswith(flag):
                paths.append(os.path.join(root, file))
                if len(paths) == num_of_required_paths:
                    return paths
    return paths


class Unit:
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent
        # other params such lineno, col offset
        # block info

    def __str__(self):
        # string representation
        return ast.dump(self.node)

    def search_for_pos(self, stmt_lst, current_stmt):
        for i, stmt in enumerate(stmt_lst):
    #        print(astor.to_source(stmt), astor.to_source(current_stmt))
            if stmt == current_stmt:
                return i
        return -1

    def insert_stmt_before(self, new_stmt):
        if self.parent is not None and hasattr(self.parent, "body"):
            try:
                pos = self.parent.body.index(self.node)
                self.parent.body.insert(pos, new_stmt)
            except Exception as e:
                raise Exception("Insertion Failure")
        else:
            raise Exception("Error!!")

    def insert_stmts_before(self, new_stmts):
        if self.parent is not None and hasattr(self.parent, "body"):
            try:
                pos = self.parent.body.index(self.node)
               
                self.parent.body[pos:pos+1] = new_stmts
            except Exception as e:
                raise Exception("Insertion Failure")
        else:
            raise Exception("Error!!")
    def insert_after(self, new_stmt):
        if self.parent is not None and hasattr(self.parent, "body"):
            try:
                pos = self.parent.body.index(self.node)
                self.parent.body.insert(pos+1, new_stmt)
            except Exception as e:
                raise Exception("Insertion Failure")
        else:
            raise Exception("Error!!")

    def remove():
        return None

    def replace():
        return 0

def UnitWalker(module_node):
    # this code is adapted from the implementation of ast.walk
    # it does only handle statement level
    # offset to the first
    from collections import deque
    init_stmts = []
    for node in module_node.body:
        node.parent = module_node
        init_stmts += [node]
    todo = deque(init_stmts)
    parent = module_node
    while todo:
        node = todo.popleft()
        yield Unit(node, node.parent)
        if hasattr(node, "body"):
            for ch_node in  node.body:
                ch_node.parent = node
                todo.append(ch_node)


class StmtIterator:

    def __init__(self, src):
        self.src = src
        self.ast = ast.parse(src)
        assert hasattr(self.ast, "body")
        self.working_stack = [self.ast.body]

    def __iter__(self):
        return self

    def __next__(self): 
        # needs to return statement with the block information to allow
        # insertion and removal
        current_loc = 0
        raise Exception("StopIteration")

    def insert_before(self, new_stmt):
        pass

    def insert_after(self, new_stmt):
        pass

    def remove(self):
        pass

    def replace(self, new_stmt):
        pass

