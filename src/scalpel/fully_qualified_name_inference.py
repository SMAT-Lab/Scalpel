"""Fully Qualified Name Inference module  in Python static code analysis is the process of determining the fully qualified name of an object or entity from its context. 
This module provides an option to perform either perform full name inference as implemented in Scalpel or further perform dynamic analysis, which is inherited from HeaderGen
https://doi.org/10.48550/arXiv.2301.04419."""


from scalpel.core.mnode import MNode
import re
import inspect
import importlib
import pathlib



class FullyQualifiedNameInference:
    def __init__(self, src = None, is_path = False, path = None, dynamic = False):
        # sourcery skip: raise-specific-error
        self.is_path = is_path
        self.path = path
        self.is_dynamic = dynamic


        if src is None and self.path is None:
            raise Exception('Either a source code or a path to a source code should be provided')

        self.src = pathlib.Path(f"src_code/{src}").read_text() if self.is_path else src
            
    def infer(self):
        mnode = MNode("local")
        mnode.source = self.src
        mnode.gen_ast()
        # parse all function calls
        self.func_calls = mnode.parse_func_calls()
        # obtain the imported name information
        self.import_dict = mnode.parse_import_stmts()
        #print(self.func_calls)

        for call_info in self.func_calls:
            call_name = call_info["name"]
            dotted_parts = call_name.split(".")
            # if this function calls is from a imported module
            if dotted_parts[0] in self.import_dict:
                dotted_parts = [self.import_dict[dotted_parts[0]]] + dotted_parts[1:]
                call_name = ".".join(dotted_parts)
                if callable(call_name):
                    if self.is_dynamic:
                        call_name = self.__get_dynamic(call_name)
                    print(call_name)
                    
    
    
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
            