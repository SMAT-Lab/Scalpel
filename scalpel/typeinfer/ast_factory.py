"""
Python 3.9 2021
"""

import ast
from scalpel.core.func_call_visitor import get_func_calls, get_call_type
from scalpel.cfg import CFGBuilder
from utilities import get_type


def get_api_ref_id(import_nodes):
    id2fullname = {}  # key is the imported module while the value is the prefix
    for node in import_nodes:
        if isinstance(node, ast.Import):
            items = [nn.__dict__ for nn in node.names]
            for d in items:
                if d['asname'] is None:  # alias name not found, use its imported name
                    id2fullname[d['name']] = d['name']
                else:
                    id2fullname[d['asname']] = d['name']  # otherwise , use alias name
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            # for import from statements
            # module names are the head of a API name
            items = [nn.__dict__ for nn in node.names]
            for d in items:
                if d['asname'] is None:  # alias name not found
                    id2fullname[d['name']] = node.module + '.' + d['name']
                else:
                    id2fullname[d['asname']] = node.module + '.' + d['name']
    return id2fullname


# Rule Parser
class ParseVisitor(ast.NodeVisitor):
    def __init__(self):
        self.assign_nodes = []
        self.import_nodes = []
        self.records = []
        self.class_obj = {}
        self.alias_pair = []
        self.type_hint_pairs = []
        self.bo_test = []
        self.func_arg_db = {}
        self.call_links = []
        self.id2call = {}

    def _get_assign_records(self, node):

        id2call = {}
        for tmp_node in ast.walk(node):
            if isinstance(tmp_node, ast.Assign) and len(tmp_node.targets) == 1:
                left = tmp_node.targets[0]
                right = tmp_node.value
                if isinstance(left, ast.Name) and isinstance(right, ast.Call):
                    func_name = get_func_calls(right)[0]
                    id2call[left.id] = func_name
        all_func_names = get_func_calls(node)
        for func_name in all_func_names:
            if func_name in id2call:
                # this function call is a value of an assignment
                self.type_hint_pairs += [(id2call[func_name], "callable")]

    def visit_FunctionDef(self, node):
        self._get_assign_records(node)
        function_arg_types = get_call_type(node)
        for pair in function_arg_types:
            name, arg_type = pair
            if name in self.func_arg_db:
                self.func_arg_db[name] += [arg_type]
            else:
                self.func_arg_db[name] = [arg_type]
        self.generic_visit(node)

        return node

    def visit_Import(self, node):
        self.import_nodes.append(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.import_nodes.append(node)
        self.generic_visit(node)

    def visit_While(self, node):
        if isinstance(node.test, ast.Call):
            func_name = get_func_calls(node.test)
            func_name = func_name[0]
            self.bo_test += [func_name]
        self.generic_visit(node)

        return node

    def visit_Compare(self, node):
        left = node.left
        right = node.comparators[0]
        left_type = get_type(left)
        right_type = get_type(right)
        if left_type not in ["unknown", "ID", "subscript", "attr"] and right_type == "call":
            self.type_hint_pairs += [(get_func_calls(right)[0], left_type)]

        if right_type not in ["unknown", "ID", "subscript", "attr"] and left_type == "call":
            self.type_hint_pairs += [(get_func_calls(left)[0], right_type)]
        if left_type == "call" and right_type == "call":
            self.call_links = [(get_func_calls(left)[0],
                                get_func_calls(right)[0])]

        self.generic_visit(node)
        return node

    def visit_BinOp(self, node):
        left = node.left
        right = node.right
        left_type = get_type(left)
        right_type = get_type(right)
        if left_type not in ["unknown", "ID", "subscript", "attr"] and right_type == "call":
            self.type_hint_pairs += [(get_func_calls(right)[0], left_type)]

        if right_type not in ["unknown", "ID", "subscript", "attr"] and left_type == "call":
            self.type_hint_pairs += [(get_func_calls(left)[0], right_type)]

        if left_type == "call" and right_type == "call":
            self.call_links = [(get_func_calls(left)[0], get_func_calls(right)[0])]

        self.generic_visit(node)
        return node

    def visit_IfExp(self, node):
        if isinstance(node.test, ast.Call):
            func_name = get_func_calls(node.test)
            func_name = func_name[0]
            self.type_hint_pairs += [(func_name, "bool")]
        self.generic_visit(node)
        return node

    def visit_If(self, node):
        if isinstance(node.test, ast.Call):
            func_name = get_func_calls(node.test)
            func_name = func_name[0]
            self.bo_test += [func_name]
            self.type_hint_pairs += [(func_name, "bool")]
        self.generic_visit(node)
        return node


class SourceSplitVisitor(ast.NodeVisitor):
    def __init__(self):
        self.assign_dict = {}

    def visit_Assign(self, node):
        # this is an example
        # x, y = fun()
        if len(node.targets) > 1:
            return node
        left = node.targets[0]
        right = node.value
        if not isinstance(left, ast.Name):
            return node
        if left.id not in self.assign_dict:
            self.assign_dict[left.id] = [right]
        else:
            self.assign_dict[left.id] += [right]

        return node

    def do_copy_(self):
        pass

    def visit_FunctionDef(self, node):
        return node


class ClassSplitVisitor(ast.NodeVisitor):
    def __init__(self):
        self.fun_nodes = []
        self.class_assign_records = {"init_arg_name_lst": []}

    def visit_FunctionDef(self, node):
        self.fun_nodes.append(node)
        if node.name == '__init__':
            for arg in node.args.args:
                self.class_assign_records["init_arg_name_lst"] += [arg.arg]
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Attribute):
                    left = get_attr_name(stmt.targets[0])
                    if left not in self.class_assign_records:
                        self.class_assign_records[left] = [stmt.value]
        return node

    def visit_ClassDef(self, node):
        for tmp_node in node.body:
            if not isinstance(tmp_node, ast.Assign):
                continue
            if len(tmp_node.targets) > 1:
                continue
            left = tmp_node.targets[0]
            right = tmp_node.value
            if isinstance(left, ast.Name):
                if left.id not in self.class_assign_records:
                    self.class_assign_records[left.id] = [right]
                else:
                    self.class_assign_records[left.id] += [right]
            else:
                pass  # what if it is self.xxx like  TBD
        self.generic_visit(node)


def get_attr_name(node):
    if isinstance(node, ast.Call):
        # to be test
        return get_attr_name(node.func)
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return get_attr_name(node.value) + "." + node.attr
    elif isinstance(node, ast.Subscript):
        return ""
    return ""  # other types


class ReturnStmtVisitor(ast.NodeVisitor):

    def __init__(self):
        self.ast_nodes = []
        self.assign_records = {}
        self.local_assign_records = {}
        self.class_assign_records = {"init_arg_name_lst": []}
        self.inner_fun_names = []
        self.stem_from = []
        self.n_returns = 0
        self.r_types = []
        self.init_args = []

    def import_assign_records(self, assign_records):
        self.assign_records = assign_records

    def import_class_assign_records(self, assign_records):
        self.class_assign_records = assign_records

    def visit_FunctionDef(self, node):
        args = node.args
        for arg in args.args:
            self.args.append(arg.arg)
        for tmp_node in ast.walk(node):
            if not isinstance(tmp_node, (ast.Assign, ast.AnnAssign)):
                continue

            left, right = None, None
            if isinstance(tmp_node, ast.Assign):
                if len(tmp_node.targets) == 1:
                    left = tmp_node.targets[0]
                    right = tmp_node.value
                else:
                    continue
            if isinstance(tmp_node, ast.AnnAssign):
                left = tmp_node.target
                right = tmp_node.value

            if isinstance(left, ast.Name):
                if left.id not in self.local_assign_records:
                    self.local_assign_records[left.id] = [right]
                else:
                    self.local_assign_records[left.id] += [right]

            if isinstance(left, ast.Attribute):
                left_name = get_attr_name(left)
                if left_name not in self.local_assign_records:
                    self.local_assign_records[left_name] = [right]
                else:
                    self.local_assign_records[left_name] += [right]
            else:
                pass
        self.type_infer_CFG(node)
        return node

    def visit_Yield(self, node):
        self.n_returns += 1
        self.r_types += ['generator']
        return node

    @staticmethod
    def get_return_value(block):
        for stmt in block.statements:
            if isinstance(stmt, ast.Return):
                return stmt.value
        return None

    def backward(self, cfg, block, return_value):
        is_visited = set()

        if return_value is None:
            self.r_types += ["empty"]
            return
        elif isinstance(return_value, ast.Name):
            if return_value.id == "self":
                self.r_types += ["self"]
                return
            elif return_value.id in self.inner_fun_names:
                self.r_types += ["callable"]
                return

        init_val = cfg.backward(block, return_value, is_visited, None)
        type_val = get_type(init_val)

        if init_val is None and isinstance(return_value, ast.Name):
            if return_value.id in self.args:
                self.r_types += ['input']
            if return_value.id in self.args:
                self.r_types += ['input']
                return

                # name object or attribute object
        if type_val in ["ID", "attr"]:
            lookup_name = node.id if type_val == "ID" else get_attr_name(init_val)
            if lookup_name in self.local_assign_records:
                right = self.local_assign_records[lookup_name][-1]
                self.type_infer(right)
            elif lookup_name.lstrip("self.") in self.class_assign_records:
                right = self.class_assign_records[lookup_name[5:]][-1]
                self.type_infer(right)
                # use self.name again
            elif lookup_name in self.class_assign_records:
                right = self.class_assign_records[lookup_name][-1]
                self.type_infer(right)

            elif lookup_name in self.assign_records:
                # TBD inspect
                right = self.assign_records[lookup_name][-1]
                self.type_infer(right)
            else:
                pass
        elif type_val == "call":
            # if func_name in ['copy', 'deepcopy', 'copy.copy', 'copy.deepcopy']:
            #    pass
            func_name = get_func_calls(init_val)
            func_name = func_name[0]

            first_part = func_name.split('.')[0]
            if func_name == "self.__class__":
                # same as class itself
                self.r_types += ['self']
            elif first_part != 'self' and first_part in self.args:
                self.r_types += ['input']
            elif first_part != 'self' and first_part in self.class_assign_records["init_arg_name_lst"]:
                self.r_types += ['input']
            else:
                self.stem_from.append(func_name)  # if this is a function call # self.r_types += [type_val]

        elif type_val == "subscript":
            if isinstance(init_val, ast.Name):
                if init_val.id in self.args or init_val.id in self.class_assign_records["init_arg_name_lst"]:
                    self.r_types += ['input']
        else:
            # known type
            self.r_types += [type_val]

    def type_infer_CFG(self, node):
        new_body = []
        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                self.inner_fun_names.append(stmt.name)
            if isinstance(stmt, ast.ClassDef):
                self.inner_fun_names.append(stmt.name)
            else:
                for small_stmt in ast.walk(stmt):
                    if isinstance(small_stmt, ast.Return):
                        self.n_returns += 1
                    elif isinstance(small_stmt, ast.Yield):
                        self.n_returns += 1
                        self.r_types += ["generator"]
                new_body.append(stmt)

        tmp_fun_node = ast.Module(body=new_body)
        cfg = CFGBuilder().build(node.name, tmp_fun_node)
        for block in cfg.finalblocks:
            return_value = self.get_return_value(block)
            if isinstance(return_value, ast.IfExp):
                self.backward(cfg, block, return_value.body)
                self.backward(cfg, block, return_value.orelse)
            else:
                self.backward(cfg, block, return_value)

    def query_assign_records(self, var_id):
        if var_id in self.local_assign_records:
            # this includes alias analysis
            right = self.local_assign_records[var_id][-1]
            return right
        elif var_id in self.class_assign_records:
            right = self.class_assign_records[var_id][-1]
            return right
            # self.type_infer(right)
        elif var_id in self.assign_records:
            # TBD inspect
            right = self.assign_records[var_id][-1]
            return right
            # self.type_infer(right)
        return None

    def type_infer(self, node):
        type_val = get_type(node)
        if type_val == 'ID':
            right = self.query_assign_records(node.id)
            if right is not None:
                self.type_infer(right)
            else:
                pass
        elif type_val == 'call':
            func_name = get_func_calls(node)
            func_name = func_name[0]
            first_part_name = func_name.split('.')[0]

            if first_part_name in self.args or first_part_name in self.class_assign_records["init_arg_name_lst"]:
                self.r_types += ['input']
            elif func_name in self.args:
                self.r_types += ['input']
            elif func_name in self.class_assign_records["init_arg_name_lst"]:
                self.r_types += ['input']
            elif func_name in ['copy', 'deepcopy', 'copy.copy', 'copy.deepcopy']:
                pass
            else:
                self.stem_from.append(func_name)  # if this is a function call # self.r_types += [type_val]
        elif type_val == "subscript":
            if isinstance(node.value, ast.Name) and node.value.id in self.args:
                self.r_types += ['input']
        else:
            # known type
            self.r_types += [type_val]

    def clear(self):
        self.r_types = []
        self.n_returns = 0
        self.args = []
        self.stem_from = []
        self.ast_nodes = []
        self.inner_fun_names = []
        self.local_assign_records = {}

    def clear_all(self):
        self.clear()
        self.class_assign_records = {}
