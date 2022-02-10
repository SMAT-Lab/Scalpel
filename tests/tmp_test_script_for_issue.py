from scalpel.typeinfer.typeinfer import TypeInference


inferer = TypeInference(name='type_infer_example.py', entry_point='./test-cases/typeinfer_real_cases/requests_case2.py')
inferer.infer_types()
inferred = inferer.get_types()
print(inferred)
