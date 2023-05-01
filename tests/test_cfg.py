import textwrap
from scalpel.cfg import CFGBuilder
import ast

def test_cfg_with_all_possible_branches():
    src = textwrap.dedent("""
        def f():
            x = 1
            try:
                a = open("a.txt", "r")
                x = 2
                a.close()
            except IOError:
                x = 3
            except:
                x = 4
            else:
                x = 5
            finally:
                y = 1
            
            y += 6
            return x + y    
        """)
    ast_f = ast.parse(src).body[0]
    print(ast_f)

    cfg = CFGBuilder().build_from_src(name="top_level", src=src)

    f_name = "f"
    fct_cfg = None
    for (_, fun_name), fun_cfg in cfg.functioncfgs.items():
        if fun_name == f_name:
            fct_cfg = fun_cfg
            break

    assert fct_cfg is not None
    cfg = fct_cfg

    assert len(cfg.get_all_blocks()) == 7
    assert isinstance(cfg.get_all_blocks()[0].statements[-1], ast.Try)
    assert isinstance(cfg.get_all_blocks()[1].statements[-1].value, ast.Call)
    assert isinstance(cfg.get_all_blocks()[2].statements[-1], ast.Assign)
    assert isinstance(cfg.get_all_blocks()[3].statements[-1], ast.Assign)
    assert isinstance(cfg.get_all_blocks()[4].statements[-1], ast.Assign)
    assert isinstance(cfg.get_all_blocks()[5].statements[-1], ast.Assign)
    assert isinstance(cfg.get_all_blocks()[6].statements[0], ast.AugAssign)
    assert isinstance(cfg.get_all_blocks()[6].statements[-1], ast.Return)

    
    assert len(cfg.get_all_blocks()[0].exits) == 3
    assert cfg.get_all_blocks()[0].exits[0].target == cfg.get_all_blocks()[1]
    assert isinstance(cfg.get_all_blocks()[0].exits[0].exitcase, ast.Constant) and cfg.get_all_blocks()[0].exits[0].exitcase.value == True

    assert cfg.get_all_blocks()[0].exits[1].target == cfg.get_all_blocks()[2]
    assert isinstance(cfg.get_all_blocks()[0].exits[1].exitcase, ast.Name) and cfg.get_all_blocks()[0].exits[1].exitcase.id == "IOError"

    assert cfg.get_all_blocks()[0].exits[2].target == cfg.get_all_blocks()[3]
    assert cfg.get_all_blocks()[0].exits[2].exitcase is None

    assert len(cfg.get_all_blocks()[1].exits) == 1
    assert cfg.get_all_blocks()[1].exits[0].target == cfg.get_all_blocks()[4]
    assert cfg.get_all_blocks()[1].exits[0].exitcase is None

    assert len(cfg.get_all_blocks()[2].exits) == 1
    assert cfg.get_all_blocks()[2].exits[0].target == cfg.get_all_blocks()[5]
    assert cfg.get_all_blocks()[2].exits[0].exitcase is None

    assert len(cfg.get_all_blocks()[3].exits) == 1
    assert cfg.get_all_blocks()[3].exits[0].target == cfg.get_all_blocks()[5]
    assert cfg.get_all_blocks()[3].exits[0].exitcase is None

    assert len(cfg.get_all_blocks()[4].exits) == 1
    assert cfg.get_all_blocks()[4].exits[0].target == cfg.get_all_blocks()[5]
    assert cfg.get_all_blocks()[4].exits[0].exitcase is None

    assert len(cfg.get_all_blocks()[5].exits) == 1
    assert cfg.get_all_blocks()[5].exits[0].target == cfg.get_all_blocks()[6]
    assert cfg.get_all_blocks()[5].exits[0].exitcase is None

    assert len(cfg.get_all_blocks()[6].exits) == 0
