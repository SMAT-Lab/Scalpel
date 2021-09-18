"""
Tomas Bolger 2021
Python 3.9
Automated Type Inference
"""

import os
import re
import ast
import astunparse

from scalpel.typeinfer.utilities import (
    parse_module,
    get_api_ref_id,
    is_imported_fun,
    rename_from_name,
    is_valid_call_link
)
from scalpel.typeinfer.archive.ast_factory import (
    SourceSplitVisitor,
    ReturnStmtVisitor,
    ClassSplitVisitor
)
from scalpel.import_graph.import_graph import (
    ImportGraph,
    Tree
)


class Infer:

    def __init__(self, name: str, entry_point: str):
        self.name = name
        self.entry = entry_point
        if self.entry.endswith(".py"):
            # Singular Python file
            self.root = Tree(os.path.basename(self.entry))
        else:
            # Directory of files
            self.root = Tree(self.name)

        self.import_graph = None
        self.leaves = []

        # Build a graph of the directory
        cwd = os.getcwd()
        os.chdir(os.path.dirname(self.entry))  # Go to the entry point directory
        self.import_graph = ImportGraph(self.entry, self.root)
        self.import_graph.build_dir_tree(self.root)
        os.chdir(cwd)  # Change back to current working directory

        # Build the leaf stack
        queue = [self.root]
        while len(queue) > 0:
            node = queue.pop(0)
            if node.name.endswith('.py'):
                self.leaves.append(node)
            queue.extend(node.children)

    def __process_file(self, file_path):
        node_type_dict, node_type_comment, node_type_gt, type_stem_links = {}, {}, {}, {}
        stem_from_dict = {}
        class2base = {}

        tree = self.generate_ast(file_path)
        if tree is None:
            return node_type_dict, node_type_gt, type_stem_links, node_type_comment

        split_visitor = SourceSplitVisitor()
        return_visitor = ReturnStmtVisitor()

        # Extract all function and class nodes
        split_visitor.visit(tree)
        assign_records = split_visitor.assign_dict
        return_visitor.import_assign_records(assign_records)
        all_methods, all_classes, import_nodes = parse_module(tree)  # TODO: Is this function really needed?
        import_dict = get_api_ref_id(import_nodes)

        # Loop through all function nodes
        for method_node in all_methods:
            method_src = astunparse.unparse(method_node)

            # Get method header comment
            matches = re.findall(r"\'(.+?)\'", method_src)
            comment = ''
            if len(matches) > 0:
                comment = matches[0]

            method_name = method_node.name

            return_visitor.clear()
            return_visitor.visit(method_node)

            # Write collected details for this method so far
            node_type_comment[method_name] = comment
            node_type_dict[method_name] = None
            node_type_gt[method_name] = None

            # Check to see whether this function actually returns
            if return_visitor.n_returns == 0:
                continue

            # Write final collected details for the method
            r_types = return_visitor.r_types
            node_type_dict[method_name] = r_types
            stem_from_dict[method_name] = return_visitor.stem_from
            node_type_gt[method_name] = method_node.returns

        # Loop through the class nodes
        for class_node in all_classes:
            class_visitor = ClassSplitVisitor()
            class_visitor.visit(class_node)
            class_name = class_node.name

            # Check to see if there are more than one base class
            if len(class_node.bases) > 0:
                if isinstance(class_node.bases[0], ast.Name):
                    class2base[class_name] = class_node.bases[0].id

            class_assign_records = class_visitor.class_assign_records
            return_visitor.clear_all()
            return_visitor.import_assign_records(class_assign_records)

            for function_node in class_visitor.fun_nodes:
                function_name = f"{class_name}.{function_node.name}"
                function_src = astunparse.unparse(function_node)

                # Get method header information
                comment = ""
                matches = re.findall(r"\'(.+?)\'", function_src)
                if len(matches) > 0:
                    comment = matches[0]

                return_visitor.clear()
                return_visitor.visit(function_node)

                # Write information collected so far
                node_type_comment[function_name] = comment
                node_type_dict[function_name] = None
                node_type_gt[function_name] = None

                # Check to see if the function actually returns anything
                if return_visitor.n_returns == 0:
                    continue

                r_types = return_visitor.r_types
                node_type_dict[function_name] = r_types
                stem_from_dict[function_name] = return_visitor.stem_from
                node_type_gt[function_name] = function_node.returns

        for function_name, stems in stem_from_dict.items():
            stems = list(dict.fromkeys(stems))
            for from_name in stems:
                if from_name.find('self.') == 0:
                    # From the same class
                    type_stem_links[function_name] = (self, from_name)
                elif from_name.find('super.') == 0:
                    # From super class
                    class_name = function_name.split('.')[0]  # Super class name
                    if class_name in class2base:
                        base_name = class2base[class_name]
                        if base_name in import_dict:
                            type_stem_links[function_name] = (
                                import_dict[base_name], base_name + from_name.lstrip('super'))
                        else:
                            type_stem_links[function_name] = ('base', base_name + from_name.lstrip('super'))
                    else:
                        # Can be from other libraries as well
                        pass
                elif from_name in node_type_dict:
                    type_stem_links[function_name] = ('local', from_name)
                else:
                    import_path = is_imported_fun(from_name, import_dict)
                    if import_path is not None:
                        type_stem_links[function_name] = (import_path, from_name)

        # Return collected details
        return node_type_dict, node_type_gt, type_stem_links, node_type_comment

    def process_leaves(self):
        """
        Process each file in the directory
        """
        for node in self.leaves:
            node_type_dict, node_type_gt, type_stem_links, node_type_comment = self.__process_file(node.source)
            node.node_type_dict = node_type_dict
            node.node_type_gt = node_type_gt
            node.call_links = type_stem_links

    def connect_leaves(self):
        for node in self.leaves:
            for function_name, (from_where, from_name) in node.call_links.items():
                # Same module
                if node.node_type_dict[function_name] is None:
                    continue

                if from_where in ['self', 'local', 'base']:
                    from_name = rename_from_name(from_where, from_name, function_name)
                    if from_name in node.node_type_dict and node.node_type_dict[from_name] is not None:
                        t_vals_tmp = node.node_type_dict[from_name]
                        if is_valid_call_link(t_vals_tmp):
                            node.node_type_dict[function_name] += t_vals_tmp
                else:
                    visit_path = from_name.split('.')
                    if len(visit_path) == 1 and visit_path[0] == self.import_graph.root.name:
                        dst_node = self.import_graph.root
                    else:
                        dst_node = self.import_graph.go_to_that_node(node, from_where.split('.')[0:-1])

                    if dst_node is not None:
                        if dst_node.node_type_dict is not None:
                            if from_name in dst_node.node_type_dict and dst_node.node_type_dict[from_name] is not None:
                                t_vals_tmp = dst_node.node_type_dict[from_name]
                                if is_valid_call_link(t_vals_tmp):
                                    node.node_type_dict[function_name] += t_vals_tmp
                    else:
                        # TODO: Check what effect this has
                        # This is a library call 3call be propagated to other affected calls
                        node.node_type_dict[function_name] += ["3call"]

    @staticmethod
    def find_class_by_attr(module_records, attrs):
        if len(attrs) < 5:
            return None
        class_names = [item.split('.')[0] for item in module_records if len(item.split('.')) == 2]
        class_names = list(set(class_names))
        for c_name in class_names:
            if all([(c_name + '.' + x) in module_records for x in attrs]):
                return c_name

        return None

    @staticmethod
    def generate_ast(source):
        try:
            return ast.parse(source, mode='exec', type_comments=True)
        except Exception as e:
            print(e)
            return None


def infer_types(file_path):
    inferrer = Infer(file_path, file_path)
    inferrer.process_leaves()
