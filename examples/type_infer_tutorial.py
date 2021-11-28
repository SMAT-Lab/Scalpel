from scalpel.typeinfer.typeinfer import TypeInference

inferer = TypeInference(name='type_infer_example.py', entry_point='./type_infer_example.py')
inferer.infer_types()
inferred = inferer.get_types()
print(inferred)