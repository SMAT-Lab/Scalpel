import os
from scalpel.typeinfer.typeinfer import TypeInference

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
inferer = TypeInference(name='type_infer_example.py', entry_point=os.path.join(current_directory,'type_infer_example.py'))
inferer.infer_types()
inferred = inferer.get_types()
print(inferred)