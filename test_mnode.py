from scalpel.core.mnode import MNode

def test_mnode():
    source = open("test-cases/mnode_case.py").read()
    mnode = MNode("local")
    mnode.source = source
    mnode.gen_ast()

    # Test gent_ast()
    assert mnode.ast is not None

    # Test parse_vars()
    var_records = mnode.parse_vars()
    #print(var_records)
    assert next(item for item in var_records if item["name"] == "y")["lineno"] == 20
    assert next(item for item in var_records if item["name"] == "y")["usage"] == 'store'

    # Test parse_func_calls()
    func_calls = mnode.parse_func_calls("Test2.fun")
    assert next(item for item in func_calls if item["name"] == "A.xx")["params"] == ['x', 'y']
    #print(func_calls)

    # Test parse_import_stmts()
    import_stms = mnode.parse_import_stmts()
    assert import_stms['A'] == 'X.A'
    assert import_stms['d'] == 'Y.D'
    print(import_stms)

    # Test parse_func_defs()
    func_defs = mnode.parse_func_defs()
    assert next(item for item in func_defs if item["name"] == "AA")["scope"] == 'mod'
    assert next(item for item in func_defs if item["name"] == "fun")["scope"] == 'Test2'
    #assert next(item for item in func_defs if item["name"] == "AA")["arg"] == ['a','b']
    #print(func_defs)

    # Test parse_function_body()
    #func_body = mnode.parse_function_body()
    #assert len(func_body[0]['AA']['assign_pairs']) == 1
    #assert next(item for item in func_body[0]['AA']['assign_pairs'] if item['var']["name"] == "x")['calls'][0]['name']=='d.xx'
    #assert func_body[1]['Test2'] == ['Test']
    #print(func_body[0]['AA'])
    #print(func_body[1])

if __name__ == "__main__":
    test_mnode()
