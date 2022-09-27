from cmath import exp
import os
import jedi
from scalpel.import_graph.import_graph import Tree, ImportGraph
from typing import List
from pathlib import Path


class TypeInferenceJedi:
    """
    Infer types for the modules accessible from the entrypoints with the help of Jedi
    """

    def __init__(self, name: str, entry_point: str):
        """
        Args:
            name: the name of the type inference analyser
            entry_point: the entry point, can be the root folder of a package or a python file
        """
        self.name = name
        self.entry_point = entry_point
        self.import_graph = None
        self.leaves = []
        self.jedi_output = {}

        # get all Python files in dir
        if os.path.isdir(entry_point):
            self.leaves = sorted(Path(entry_point).rglob("*.py"))
        else:
            self.leaves = [Path(entry_point)]

    def parse_type_hint(self, type_hint):
        # TODO: Replace this with a more sane version from the internals of Jedi
        _type = set()
        if type_hint:
            try:
                _t = type_hint.split(" -> ")[1]
                if "Union" in _t:
                    _list_of_types = (
                        _t.split("Union")[1]
                        .replace("[", "")
                        .replace("]", "")
                        .split(", ")
                    )
                    for _l_t in _list_of_types:
                        _type.add(_l_t)
                elif _t.endswith("()"):
                    _type.add("callable")
                else:
                    _type.add(_t)
            except Exception as e:
                print("Unable to parse type hint")
                pass

        return _type

    def find_types_by_execute(self, jedi_obj):
        _type = set()
        _try_type_hint = None

        try:
            _try_type_hint = self.parse_type_hint(jedi_obj.get_type_hint())
        except Exception as e:
            print("Unable to fetch type hint from Jedi")

        if _try_type_hint:
            _type = _try_type_hint
        else:
            for _name in jedi_obj.execute():
                _type = self.parse_type_hint(_name.get_type_hint())

                if not _type:
                    # Find builtin types
                    if _name.module_name == "builtins":
                        _type.add(_name.name)

        return _type

    def get_function_name(self, jedi_obj):
        try:
            func_name = ".".join(
                jedi_obj.full_name.replace(jedi_obj.module_name, "").split(".")[1:]
            )
        except Exception as e:
            print("full_name not found in jedi_obj?")
            func_name = jedi_obj.name

        return func_name

    def infer_types(self):
        """
        Infer the types for the modules accessible from the entrypoint
        """
        output_inferred = []

        for node in self.leaves:
            var_names = {}
            # self.code = open(node).read()
            for _name in jedi.Script(path=str(node)).get_names(
                all_scopes=1, definitions=1
            ):
                var_names[f"{_name.name}:{_name.line}_{_name.column}"] = {
                    "line": _name.line,
                    "column": _name.column,
                    "jedi_obj": _name,
                }

            for var, pos in var_names.items():
                # TODO: Should this be really skipped?
                if var.startswith(("self", "__init__")):
                    continue

                # HACK: Currently following a two-step approach to fetch types from Jedi.
                # Typically, we should be able to directly infer on the 'jedi_obj', but
                # there is a performance issue of Script object after a few iterations.
                # Creating new Script obj everytime to mitigate this as suggested by author.
                _infer = jedi.Script(path=str(node)).infer(pos["line"], pos["column"])
                if _infer:
                    for inferred in _infer:
                        if inferred.type == "function":
                            # _type = self.parse_type_hint(inferred.get_type_hint())
                            # if not _type:
                            #     self.find_types_by_execute(inferred)

                            _type = self.find_types_by_execute(inferred)

                            _info = {
                                "file": node.name,
                                "line_number": pos["line"],
                                "function": self.get_function_name(inferred),
                                "type": _type if _type else {"any"},
                            }

                            if _type:
                                output_inferred.append(_info)

                        elif inferred.type == "instance":
                            try:
                                _type = inferred.get_type_hint()
                            except Exception as e:
                                print("Unable to fetch type hint from Jedi")
                                _type = None

                            if not _type:
                                # Find builtin types
                                if inferred.module_name == "builtins":
                                    _type = inferred.name

                            _info = {
                                "file": node.name,
                                "line_number": pos["line"],
                                "variable": var.split(":")[0],
                                "function": self.get_function_name(
                                    pos["jedi_obj"].parent()
                                ),
                                "type": {_type},
                            }

                            if _type:
                                output_inferred.append(_info)

                        elif inferred.type == "param":
                            _type = inferred.get_type_hint()
                            _info = {
                                "file": node.name,
                                "line_number": pos["line"],
                                "variable": var.split(":")[0],
                                "function": self.get_function_name(
                                    pos["jedi_obj"].parent()
                                ),
                                "type": {_type},
                            }

                            if _type:
                                output_inferred.append(_info)

                        elif inferred.type == "class":
                            pass

                else:
                    if pos["jedi_obj"].type == "param":
                        _type = pos["jedi_obj"].get_type_hint()
                        _info = {
                            "file": node.name,
                            "line_number": pos["line"],
                            "parameter": var.split(":")[0],
                            "function": self.get_function_name(
                                pos["jedi_obj"].parent()
                            ),
                            "type": {_type if _type else "any"},
                        }

                        output_inferred.append(_info)

            self.output_inferred = output_inferred

    def get_types(self) -> List[dict]:
        """
        Get the inferred type information in a list of dictionaries
        """
        return self.output_inferred
