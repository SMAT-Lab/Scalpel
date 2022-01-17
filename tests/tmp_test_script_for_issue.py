from scalpel.typeinfer.typeinfer import TypeInference


inferer = TypeInference(name='type_infer_example.py', entry_point='./test-cases/typeinfer_real_cases/requests_case1.py')
inferer.infer_types()
inferred = inferer.get_types()
print(inferred)

inferer = TypeInference(name='type_infer_example2.py', entry_point='./test-cases/typeinfer_real_cases/pydriller_case2.py')
inferer.infer_types()
inferred = inferer.get_types()
print(inferred)