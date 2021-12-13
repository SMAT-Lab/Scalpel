"""
This module is the main module of typeinfer. The module contains a single class named TypeInference which processes
files and infer types.
"""

import os
import ast
import astunparse
from typing import List
from pprint import pprint

from scalpel.typeinfer.visitors import get_call_type
from scalpel.typeinfer.classes import ProcessedFile, ScalpelVariable
from scalpel.typeinfer.analysers import (
    ImportTypeMap,
    SourceSplitVisitor,
    ClassSplitVisitor,
    ReturnStmtVisitor,
    HeuristicParser,
    Heuristics,
    VariableAssignmentMap
)
from scalpel.import_graph.import_graph import Tree, ImportGraph
from scalpel.typeinfer.utilities import (
    generate_ast,
    parse_module,
    get_api_ref_id,
    get_function_comment,
    is_imported_fun,
    is_valid_call_link,
    rename_from_name,
    is_done,
    find_class_by_attr,
)

def process_code_with_heuristics(node):
    def pick_type(type_lst):
        base_type_names = ["Num", "Set", "List", "Tuple", "Dict", "Str", "NameConstant"]
        new_type_lst = []
        type_hint_pair_list = []
        length = len(type_lst[0])
        if length == 0:
            return []
        type_lst = filter(lambda x: len(x) == length, type_lst)
        for i in range(length):
            i_th = [t[i] for t in type_lst]
            new_type_lst += [None]
            for tmp in i_th:
                if tmp in base_type_names:
                    new_type_lst[-1] = tmp
                    break
            for tmp in i_th:
                if isinstance(tmp, tuple) and tmp[0] == "Call":
                    if new_type_lst[i] is not None:
                        type_hint_pair_list += [(tmp[1], new_type_lst[i])]

        return type_hint_pair_list

    try:
        tree = ast.parse(node.source, mode='exec')
        visitor = HeuristicParser(node)
        visitor.visit(tree)
        func_arg_db = {}
        function_arg_types = get_call_type(tree)
        type_hint_pairs = visitor.type_hint_pairs
        all_call_names = []
        for pair in function_arg_types:
            name, arg_type = pair
            name_parts = name.split('.')
            name = ".".join(name_parts)
            all_call_names += [name]
            if name in func_arg_db:
                func_arg_db[name] += [arg_type]
            else:
                func_arg_db[name] = [arg_type]
        for func, arg_type in func_arg_db.items():
            type_hint_pairs += pick_type(arg_type)
        return type_hint_pairs, visitor.call_links, all_call_names
    except (SyntaxError, UnicodeDecodeError):
        return {}, {}, []


class TypeInference:
    """
    Infer types for the modules accessible from the entrypoints with the help of a set of heuristic functions
    """

    def __init__(self, name: str, entry_point: str):
        """
        Args:
            name: the name of the type inference analyser
            entry_point: the entry point, can be the root folder of a package or a python file
        """
        self.name = name
        self.entry_point = entry_point
        self.root_node = Tree(os.path.basename(self.entry_point))
        self.import_graph = None
        self.leaves = []

        # Build graph of the directory
      
        self.import_graph = ImportGraph(self.entry_point)
        self.import_graph.build_dir_tree()
        self.leaves = self.import_graph.get_leaf_nodes()

    def infer_types(self):
        """
        Infer the types for the modules accessible from the entrypoint
        """

        # Loop through leaves
        for node in self.leaves:
            processed_file = self.process_file(node.source)
            node.node_type_dict = processed_file.type_dict
            node.node_type_gt = processed_file.type_gt
            node.call_links = processed_file.type_stem_links
            node.static_assignments = processed_file.static_assignments
            node.line_numbers = processed_file.line_numbers
            node.imports = processed_file.imports
           
        for node in self.leaves:
            type_hint_pairs, client_call_link, all_call_names = process_code_with_heuristics(node)
            for pair in type_hint_pairs:
                if pair is None:
                    continue
                function_name, t_val = pair
                if t_val in ['call', 'input']:
                    # TODO: Why do this?
                    continue

                # Type hints are known
                if function_name in node.node_type_dict and node.node_type_dict[function_name] is not None:
                    if "input" in node.node_type_dict[function_name]:
                        node.node_type_dict[function_name] = [t_val]
                    if "3call" in node.node_type_dict[function_name]:
                        node.node_type_dict[function_name] = [t_val]
                    if "unknown" in node.node_type_dict[function_name]:
                        node.node_type_dict[function_name] = [t_val]
                    else:
                        node.node_type_dict[function_name] += [t_val]

                # Call pairs
                for call_pair in client_call_link:
                    if call_pair is None:
                        continue
                    function1, function2 = call_pair
                    # Is this the same module
                    if function1 in node.node_type_dict and function2 in node.node_type_dict:
                        # They share with each other
                        function1_t_val = node.node_type_dict[function1]
                        function2_t_val = node.node_type_dict[function2]

                        if is_done(function1_t_val) and (not is_done(function2_t_val)):
                            node.node_type_dict[function2] = function1_t_val
                        if is_done(function2_t_val) and (not is_done(function1_t_val)):
                            node.node_type_dict[function1] = function2_t_val

                function_access_attribute_records = {}
                for call_name in all_call_names:
                    call_name_segments = call_name.split('.')
                    if len(call_name_segments) < 2:
                        continue

                    if call_name_segments[0] not in node.node_type_dict:
                        continue

                    if call_name_segments[0] not in function_access_attribute_records:
                        function_access_attribute_records[call_name_segments[0]] = [call_name_segments[1]]
                    else:
                        function_access_attribute_records[call_name_segments[0]] += [call_name_segments[1]]

                for function_name, access_attrs in function_access_attribute_records.items():
                    access_attrs = list(set(access_attrs))
                    class_inferred = find_class_by_attr(list(node.node_type_dict.keys()), access_attrs)
                    if class_inferred is not None:
                        node.node_type_dict[function_name] = [class_inferred]

        # Reconcile across all leaves
        for node in self.leaves:
            for function_name, (from_where, from_name) in node.call_links.items():
                # The same module
                if node.node_type_dict[function_name] is None:
                    continue
                # self: in the same class
                # base: from the base class
                # local: from the same module file

                if from_where in ['self', 'base', 'local']:
                    from_name = rename_from_name(from_where, from_name, function_name)
                    if from_name in node.node_type_dict and node.node_type_dict[from_name] is not None:
                        t_vals_tmp = node.node_type_dict[from_name]
                        if is_valid_call_link(t_vals_tmp):
                            node.node_type_dict[function_name] += t_vals_tmp

                # Might be from other modules
                else:
                    visit_path = from_where.split('.')
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
                        # This is a library call 3call be propagated to other affected calls
                        node.node_type_dict[function_name] += ["3call"]

    def get_types(self) -> List[dict]:
        """
        Get the inferred type information in a list of dictionaries
        """
        n_known = 0
        type_list = []
        for node in self.leaves:
            # Function returns
            for function_name, type_values in node.node_type_dict.items():
              
                added = False  # Used to check whether type has already been added to list for the loop

                if type_values is None or len(type_values) == 0:
                    continue
                #TODO: why self is recognized as any type
                for value in type_values:
                    if value in ['unknown', '3call', 'self']:
                        type_list.append({
                            'file': node.name,
                            'line_number': node.line_numbers.get(function_name),
                            'function': function_name,
                            'type': {any.__name__}
                        })
                        added = True
                        break

                if is_done(type_values) and not added:
                    n_known += 1
                    type_list.append({
                        'file': node.name,
                        'line_number': node.line_numbers.get(function_name),
                        'function': function_name,
                        'type': set(type_values)
                    })
                else:
                    type_list.append({
                        'file': node.name,
                        'line_number': node.line_numbers.get(function_name),
                        'function': function_name,
                        'type': {any.__name__}
                    })

            # Static assignments
    
            for assignment in node.static_assignments:
                if assignment.is_arg:
                    if isinstance(assignment.type,list):
                        type_list.append({
                            'file': node.name,
                            'line_number': assignment.line,
                            'parameter': assignment.name,
                            'function': assignment.function,
                            'type': set(assignment.type)
                        })
                    else:
                        type_list.append({
                            'file': node.name,
                            'line_number': assignment.line,
                            'parameter': assignment.name,
                            'function': assignment.function,
                            'type': {assignment.type}
                        })
                else:
                    if isinstance(assignment.type, list):
                        type_list.append({
                            'file': node.name,
                            'line_number': assignment.line,
                            'variable': assignment.name,
                            'function': assignment.function,
                            'type': set(assignment.type)
                        })
                    else:
                        type_list.append({
                            'file': node.name,
                            'line_number': assignment.line,
                            'variable': assignment.name,
                            'function': assignment.function,
                            'type': {assignment.type}
                        })
     
        return type_list

    @staticmethod
    def process_file(source: str):
        """
        Process and extract information from the source files with a set of heuristic functions for type inference
        """
        heuristics = Heuristics()
        processed_file = ProcessedFile()

        stem_from_dict = {}
        class2base = {}

        # Generate AST from source
        
        tree = generate_ast(source)
        if tree is None:
            return processed_file

        # Get imported types
        import_mappings, imported = ImportTypeMap(tree).map()
        processed_file.imports = import_mappings

        split_visitor = SourceSplitVisitor()
        return_visitor = ReturnStmtVisitor(imports=import_mappings)

        # Extract all function and class nodes
        split_visitor.visit(tree)
        assign_records = split_visitor.assign_dict

        return_visitor.import_assign_records(assign_records)
        
        all_methods, all_classes, import_nodes = parse_module(tree)  # TODO: This doesn't need to be a function?
        

        import_dict = get_api_ref_id(import_nodes)  # TODO: Replace with import map?

        # Loop through function nodes
        for function_node in all_methods:
            function_name = function_node.name
            processed_file.line_numbers[function_name] = function_node.lineno
            function_source = astunparse.unparse(function_node)
          

            # Variable assignments
            assignments = VariableAssignmentMap(function_node, imports=import_mappings).map()
            for assignment in assignments:
                assignment.function = function_node.name
            processed_file.static_assignments.extend(assignments)

            # Heuristic 5
            heuristics.heuristic_five(
                import_mappings=import_mappings,
                processed_file=processed_file,
                function_node=function_node
            )

            # Heuristic 8
            function_params = [a for a in processed_file.static_assignments if a.is_arg]
            heuristics.heuristic_eight(
                ast_tree=tree,
                function_name=function_name,
                function_params=function_params
            )
            heuristics.heuristic_twelve(
                function_node=function_node,
                function_params=function_params
            )


            # Heuristic 7
            heuristics.heuristic_seven(
                processed_file=processed_file,
                function_node=function_node
            )

            # Heuristic 6
            heuristics.heuristic_six(
                processed_file=processed_file,
                function_node=function_node
            )

            # Heuristic 9
            heuristics.heuristic_nine(
                import_mappings=import_mappings,
                processed_file=processed_file,
                function_node=function_node
            )

            # # Heuristic 2
            heuristics.heuristic_two(
                ast_tree=tree,
                processed_file=processed_file,
                assignments=assignments
            )

            # Heuristic 5 once more to account for newly inferred types
            heuristics.heuristic_five(
                import_mappings=import_mappings,
                processed_file=processed_file,
                function_node=function_node
            )

            # Import resolved assignments to the return visitor
            return_visitor.import_assignments(assignments)

            # Get method header comment TODO: is this needed?
            processed_file.node_type_comment[function_name] = get_function_comment(function_source)

            return_visitor.clear()
            return_visitor.visit(function_node)
            processed_file.type_dict[function_name] = None
            processed_file.type_gt[function_name] = None

            if return_visitor.n_returns == 0:
                # This function has no return
                continue

            # Function has at least one return if we reach here
            processed_file.type_dict[function_name] = return_visitor.r_types
            stem_from_dict[function_name] = return_visitor.stem_from
            processed_file.type_gt[function_name] = function_node.returns
            

        # Loop through class nodes
        class_assign_record_map = {}
        for class_node in all_classes:
            class_name = class_node.name

            class_visitor = ClassSplitVisitor()
            class_visitor.visit(class_node)

            # Check for base class type
            if len(class_node.bases) > 0:
                if isinstance(class_node.bases[0], ast.Name):
                    class2base[class_name] = class_node.bases[0].id

            class_assign_records = class_visitor.class_assign_records
            class_assign_record_map[class_name] = class_assign_records

            # Extend class assign records with super class assign records
            for superclass_name in class_visitor.bases:
                assign_records = class_assign_record_map.get(superclass_name)
                if assign_records:
                    for assignment_name, type_val in assign_records.items():
                        super_assignment = assignment_name.replace('self', 'super')
                        class_assign_records[super_assignment] = type_val

            return_visitor.clear_all()
            return_visitor.import_assign_records(class_assign_records)

            # Loop through class methods
            for function_node in class_visitor.fun_nodes:
                function_name = f"{class_name}.{function_node.name}"
                function_source = astunparse.unparse(function_node)
                processed_file.line_numbers[function_name] = function_node.lineno

                # Get method header comment TODO: Is this needed?
                processed_file.node_type_comment[function_name] = get_function_comment(function_source)

                # Variable assignments
                assignments = VariableAssignmentMap(function_node, imports=import_mappings).map()
                for assignment in assignments:
                    assignment.function = function_node.name
                processed_file.static_assignments.extend(assignments)

                # Heuristic 5
                heuristics.heuristic_five(
                    import_mappings=import_mappings,
                    processed_file=processed_file,
                    function_node=function_node
                )

                # Heuristic 8
                function_params = [a for a in processed_file.static_assignments if a.is_arg]
                heuristics.heuristic_eight(
                    ast_tree=tree,
                    function_name=function_name,
                    function_params=function_params
                )

                # Heuristic 7
                heuristics.heuristic_seven(
                    processed_file=processed_file,
                    function_node=function_node
                )

                # Heuristic 6
                heuristics.heuristic_six(
                    processed_file=processed_file,
                    function_node=function_node
                )

                # Heuristic 9
                heuristics.heuristic_nine(
                    import_mappings=import_mappings,
                    processed_file=processed_file,
                    function_node=function_node
                )

                # # Heuristic 2
                heuristics.heuristic_two(
                    ast_tree=tree,
                    processed_file=processed_file,
                    assignments=assignments
                )

                # Heuristic 5 once more to account for newly inferred types
                heuristics.heuristic_five(
                    import_mappings=import_mappings,
                    processed_file=processed_file,
                    function_node=function_node
                )

                return_visitor.clear_all()
                return_visitor.import_class_assign_records(class_assign_records)
                return_visitor.visit(function_node)
                processed_file.type_dict[function_name] = None
                processed_file.type_gt[function_name] = None

                if return_visitor.n_returns == 0:
                    # There are no returns in this method
                    continue

                processed_file.type_dict[function_name] = return_visitor.r_types
                stem_from_dict[function_name] = return_visitor.stem_from
                processed_file.type_gt[function_name] = function_node.returns

        # Loop through return statements that called another function -> see Heuristic 1
     
        for function_name, stems in stem_from_dict.items():
            stems = list(dict.fromkeys(stems))
            for from_name in stems:
                # From the same class
                if from_name.find('self.') == 0:
                    processed_file.type_stem_links[function_name] = ('self', from_name)
                elif from_name.find('super.') == 0:
                    class_name = function_name.split('.')[0]
                    if class_name in class2base:
                        base_name = class2base[class_name]
                        if base_name in import_dict:
                            processed_file.type_stem_links[function_name] = (
                                import_dict[base_name], base_name + from_name.lstrip('super'))
                        else:
                            processed_file.type_stem_links[function_name] = (
                                'base', base_name + from_name.lstrip('super'))
                    else:
                        # TODO: Can be from other libraries too, check for imported classes
                        pass
                elif from_name in processed_file.type_dict:
                    processed_file.type_stem_links[function_name] = ('local', from_name)
                else:
                    import_path = is_imported_fun(from_name, import_dict)
                    if import_path is not None:
                        processed_file.type_stem_links[function_name] = (import_path, from_name)
   
        return processed_file

    def print_types(self, functions=True, parameters=True, variables=True):
        """
        Function for printing type inference results in a formatted way
        """
        self.infer_types()
        inferred_types = self.get_types()
        for case in inferred_types:
            case_type = case.get('type')
            file_name = case.get('file')
            function = case.get('function')
            line_no = case.get('line_number')
            var_name = case.get('variable')
            param_name = case.get('parameter')
            if var_name:
                if variables:
                    # We have a variable
                    print(f"{file_name}:{line_no}: Variable {var_name} in function {function} has type {case_type}")
            elif param_name:
                if parameters:
                    # We have a parameter
                    print(f"{file_name}:{line_no}: Parameter {param_name} of function {function} has type {case_type}")
            else:
                # We have a function
                if functions:
                    if len(case_type) > 1:
                        if isinstance(case_type, str):
                            case_type = case_type
                        else:
                            case_type = f"Union[{', '.join(case_type)}]"
                    else:
                        case_type = case_type.pop()
                    print(f"{file_name}:{line_no}: Function {function} has return type {case_type}")


