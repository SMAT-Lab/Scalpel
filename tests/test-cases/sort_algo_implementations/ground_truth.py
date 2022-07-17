import ast
import json
import os

from scalpel.SSA.const import SSA
from scalpel.call_graph.pycg import CallGraphGenerator
from scalpel.call_graph.pycg import formats
from scalpel.cfg import CFGBuilder
from scalpel.typeinfer.typeinfer import TypeInference

from scalpel.util import get_path_by_ext


# Enable set to be serialized as JSON
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


target_dir = "./"
all_files = get_path_by_ext(target_dir)
for idx, fn in enumerate(all_files):
    if fn.endswith(".py") and fn != "./__init__.py":
        # Initialize the dict for ground truth
        ground_truth_dict = {"Call Graph": "", "Type Information": "", "SSA": "", "Alias": ""}
        m_ssa = SSA()
        # Generate call graph
        cg_generator = CallGraphGenerator([fn], "sort_algo_implementations")
        cg_generator.analyze()
        formatter = formats.Simple(cg_generator)
        cg = formatter.generate()
        ground_truth_dict["Call Graph"] = cg

        # Generate CFG
        cfg_builder = CFGBuilder()
        cfg = cfg_builder.build_from_file(fn, "./" + fn)

        # Generate type information
        inferrer = TypeInference(name=fn, entry_point="./" + fn)
        inferrer.infer_types()
        ground_truth_dict["Type Information"] = inferrer.get_types()

        # Generate SSA results
        ssa_results, const_dict = m_ssa.compute_SSA(cfg)
        ground_truth_dict["SSA"] = ssa_results

        # Generate alias analysis
        alias_name_pairs = []
        for name, value in const_dict.items():
            if isinstance(value, ast.Name):
                alias_name_pairs.append((name, value.id))
        ground_truth_dict["Alias"] = alias_name_pairs

        with open(fn.replace(".py", "_groundtruth.json"), "w+") as f:
            f.write(json.dumps(ground_truth_dict, cls=SetEncoder))
