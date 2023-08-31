"""
This module provides an option to perform Fully Qualified Name Resolution based on PyCG callgraph.
Optionally, hybrid analysis can be performed to obtain true full name inference. This Functionality is inherited from HeaderGen https://doi.org/10.48550/arXiv.2301.04419.
Authors: Ashwin Prasad & Rupesh Sapkota
"""


import importlib
import inspect
import os
import pathlib
import re
import sys
import types

from scalpel.call_graph.pycg import CallGraphGenerator


class FullyQualifiedNameInference:
    def __init__(self, file_path=None, dynamic=False, mod_name=None):
        if not file_path:
            print("file_path is empty")
            sys.exit(-1)

        self.imported_modules = {}
        self.file_path = os.path.abspath(file_path)
        self.file_folder = os.path.abspath(os.path.dirname(file_path))

        self.is_dynamic = dynamic
        self.mod_name = mod_name
        self.builtin_calls = True

        self.built_in_calls = []
        self.external_calls = []

        cg_generator = CallGraphGenerator([self.file_path], self.file_folder)
        cg_generator.analyze()
        self.cg = cg_generator.output()
        # Find external defs
        self.external_calls = [
            x
            for x in cg_generator.def_manager.defs
            if cg_generator.def_manager.defs[x].def_type == "EXTERNALDEF"
        ]

    def process_func_calls(self):
        processed_calls = []
        module_name = self.mod_name

        def _get_leaf_nodes(_call):
            nonlocal module_name, processed_calls

            if len(self.cg[_call]) > 0:
                for _c in self.cg[_call]:
                    if _c not in processed_calls:
                        processed_calls.append(_c)
                        _get_leaf_nodes(_c)

        for _src, _dest in self.cg.items():
            for _call in _dest:
                _get_leaf_nodes(_call)
                if _call not in processed_calls:
                    processed_calls.append(_call)

        return processed_calls

    def infer(self):
        self.func_calls = self.process_func_calls()

        if not self.is_dynamic:
            return self.func_calls

        qualified_names = []

        for call_name in self.func_calls:
            if call_name.startswith("<builtin>"):
                qualified_names.append(call_name)
            else:
                if call_name in self.external_calls:
                    full_name = self._get_dynamic(call_name)
                    qualified_names.append(full_name)
                else:
                    qualified_names.append(call_name)

        return qualified_names

    def _get_dynamic(self, func_name):
        module_name = func_name.split(".")[0]

        try:
            # Try importing the module
            if module_name not in self.imported_modules:
                self.imported_modules[module_name] = importlib.import_module(
                    module_name
                )

            # Replace the module name in the function name with the imported module
            replacement = f"self.imported_modules['{module_name}']"
            regex = f"^({module_name}?)"
            dynamic_name = eval(re.sub(regex, replacement, func_name))

            info = {}
            unwrapped_dynamic_name = inspect.unwrap(dynamic_name)
            if isinstance(unwrapped_dynamic_name, types.BuiltinFunctionType):
                info["module_name"] = module_name
                info["qualified_name"] = unwrapped_dynamic_name.__qualname__
                info["fullns"] = ".".join([info["module_name"], info["qualified_name"]])
                if module_name == "numpy":
                    if globals_ := getattr(unwrapped_dynamic_name, "__globals__", None):
                        info["module_name"] = globals_["__name__"]
                    info["fullns"] = ".".join(
                        [info["module_name"], info["qualified_name"]]
                    )

            elif module := getattr(unwrapped_dynamic_name, "__module__", None):
                info["module_name"] = module
                info["qualified_name"] = unwrapped_dynamic_name.__qualname__
                info["fullns"] = ".".join([info["module_name"], info["qualified_name"]])
                if module == "numpy":
                    if globals_ := getattr(unwrapped_dynamic_name, "__globals__", None):
                        info["module_name"] = globals_["__name__"]
                    info["fullns"] = ".".join(
                        [info["module_name"], info["qualified_name"]]
                    )

            elif objclass := getattr(unwrapped_dynamic_name, "__objclass__", None):
                info["module_name"] = objclass.__module__
                info["qualified_name"] = unwrapped_dynamic_name.__qualname__
                info["fullns"] = ".".join([info["module_name"], info["qualified_name"]])
            elif package := getattr(unwrapped_dynamic_name, "__package__", None):
                info["module_name"] = unwrapped_dynamic_name.__name__
                info["qualified_name"] = unwrapped_dynamic_name.__name__
                info["fullns"] = unwrapped_dynamic_name.__name__

            else:
                info["module_name"] = getattr(
                    unwrapped_dynamic_name, "__module__", None
                )
                info["qualified_name"] = getattr(
                    unwrapped_dynamic_name, "__qualname__", None
                )

                if full_name := self._get_qualname_from_text(dynamic_name):
                    if full_name["class"].startswith(module_name):
                        info["fullns"] = f"{full_name['class']}.{full_name['func']}"
                    else:
                        info["fullns"] = func_name  # keep original if nothing works
                else:
                    info["fullns"] = f"{info['module_name']}.{info['qualified_name']}"

            return info["fullns"]

        except ImportError:
            print(f"Module not installed: {module_name}")
            return func_name  # keep original if nothing works
        except Exception as e:
            print(f"An unknown error occurred: {e}")
            return func_name  # keep original if nothing works

    def _get_qualname_from_text(self, input_dynamic_name):
        res = {"class": None, "func": None}
        try:
            input_str = inspect.unwrap(input_dynamic_name).__repr__()
            regex_class = r"(?<=of )(.*)(?= object)"

            if re.findall(regex_class, input_str):
                res["class"] = re.findall(regex_class, input_str)[0]

            regex_func = r"(?<=method )(.*)(?= of)"
            if re.findall(regex_func, input_str):
                res["func"] = re.findall(regex_func, input_str)[0]

            return res
        except Exception as e:
            return None
