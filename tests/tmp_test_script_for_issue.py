from scalpel.typeinfer.typeinfer import TypeInference


inferer = TypeInference(name='type_infer_example.py', entry_point='./test-cases/typeinfer_real_cases/pydriller_case1.py')
inferer.infer_types()
inferred = inferer.get_types()
print(inferred)