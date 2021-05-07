import ast
from  _ast import *
import pkgutil

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
            result  += [m_name]
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




