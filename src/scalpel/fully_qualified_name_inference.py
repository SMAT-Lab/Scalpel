"""Fully Qualified Name Inference module  in Python static code analysis is the process of determining the fully qualified name of an object or entity from its context. 
This module provides an option to perform either perform full name inference as implemented in Scalpel or further perform dynamic analysis, which is inherited from HeaderGen
https://doi.org/10.48550/arXiv.2301.04419."""


from scalpel.call_graph.pycg import CallGraphGenerator
import re
import inspect
import importlib
import pathlib
import types
import os



class FullyQualifiedNameInference:
    def __init__(self, src = None, rel_path = None, dynamic = False, mod_name = None):
        
        
        cwd = os.getcwd()
        self.path = os.path.join(cwd, rel_path)
        self.is_dynamic = dynamic
        self.file_name = rel_path.split("/")[0]
        self.mod_name = mod_name
        self.builtin_calls = False
        self.built_in_calls = []
        self.external_calls = []
        cg_generator = CallGraphGenerator([self.path], self.file_name)
        cg_generator.analyze()
        self.cg = cg_generator.output()

        if src is None and self.path is None:
            print('Either a source code or a path to a source code should be provided')


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
            if module_name is not None:
                # Analyze call-sites only in the main module
                if _src.split(".")[0] == module_name:
                    for _call in _dest:
                        _get_leaf_nodes(_call)
                        if _call not in processed_calls:
                            processed_calls.append(_call)
                        
            else:
                for _call in _dest:
                    _get_leaf_nodes(_call)
                    if _call not in processed_calls:
                        processed_calls.append(_call)
                    

        return processed_calls

    def separate_func_calls(self, func_calls):
        for func_call in func_calls:
            dotted_call_names  = func_call.split(".")
            if dotted_call_names[0] == '<builtin>':
                self.built_in_calls.append(dotted_call_names[1])
            else:
                self.external_calls.append(".".join(dotted_call_names))



    def infer(self):
        
        self. func_calls  = self.process_func_calls()
        self.separate_func_calls(self. func_calls)
        
        qualified_names = []
        self.infer_func_calls = self.external_calls
        if self.builtin_calls :
            self.infer_func_calls.extend(self.built_in_calls)
            
        for call_name in self.infer_func_calls:        
            if self.is_dynamic:
                full_name = self.__get_dynamic(call_name)
                qualified_names.append(full_name)   
            else:
                qualified_names.append(call_name)
                    
        return qualified_names
                    
    
    
    def __get_dynamic(self, func_name):
        mod_name = func_name.split(".")[0]
        inspect_module_imports = {}
        try:
            inspect_module_imports[mod_name] = importlib.import_module(mod_name)
            regex = f"^({mod_name}?)"

            _dynamic_name = eval(
                        re.sub(regex, f"inspect_module_imports['{mod_name}']", func_name)
                    )


            info = {}
            if getattr(inspect.unwrap(_dynamic_name), "__module__", None):
                info["module_name"] = inspect.unwrap(_dynamic_name).__module__
                self.__extracted_from___get_dynamic_16(_dynamic_name, info)
                if info["module_name"] == "numpy":
                    if getattr(inspect.unwrap(_dynamic_name), "__globals__", None):
                        info["module_name"] = getattr(
                            inspect.unwrap(_dynamic_name), "__globals__", None
                        )["__name__"]
                    info["fullns"] = ".".join(
                        [info["module_name"], info["qualified_name"]]
                    )

            elif getattr(inspect.unwrap(_dynamic_name), "__objclass__", None):
                info["module_name"] = inspect.unwrap(
                    _dynamic_name
                ).__objclass__.__module__
                self.__extracted_from___get_dynamic_16(_dynamic_name, info)
            elif getattr(inspect.unwrap(_dynamic_name), "__package__", None):
                info["module_name"] = inspect.unwrap(_dynamic_name).__name__
                info["qualified_name"] = inspect.unwrap(_dynamic_name).__name__
                info["fullns"] = inspect.unwrap(_dynamic_name).__name__
                info["doc_string"] = inspect.getdoc(_dynamic_name)
            else:
                info["module_name"] = inspect.unwrap(_dynamic_name).__module__
                info["qualified_name"] = inspect.unwrap(_dynamic_name).__qualname__
                info["doc_string"] = inspect.getdoc(_dynamic_name)

                if full_name := self.__get_qualname_from_text(_dynamic_name):
                    if full_name["class"].startswith(mod_name):
                        info["fullns"] = ".".join(
                            [full_name["class"], full_name["func"]]
                        )
                    else:
                        info["fullns"] = func_name  # keep original if nothing works
                else:
                    info["fullns"] = ".".join(
                        [info["module_name"], info["qualified_name"]]
                    )
            return info['fullns']

        except Exception as e:
            print('module not installed')

    # TODO Rename this here and in `__get_dynamic`
    def __extracted_from___get_dynamic_16(self, _dynamic_name, info):
        info["qualified_name"] = inspect.unwrap(_dynamic_name).__qualname__
        info["fullns"] = ".".join([info["module_name"], info["qualified_name"]])
        info["doc_string"] = inspect.getdoc(_dynamic_name)
            
                
    def __get_qualname_from_text(self, input_dynamic_name):
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
            