from scalpel.cfg import CFGBuilder

src="""
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib_gen = fib()
for _ in range(10):
    next(fib_gen)
"""


def main():
    cfg = CFGBuilder().build_from_src("example", src)
    fun_cfg = cfg.functioncfgs.items()
    for (block_id, fun_name), fun_cfg in cfg.functioncfgs.items():
        if fun_name == "fib":
            graph = fun_cfg.build_visual('png')
            graph.render("function_fib_cfg", view=False)
    return 0
    #graph = cfg.build_visual('pdf')
    #graph.render("example_cfg.pdf", view=False)
    for block in cfg:
        calls = block.get_calls()
        print(calls)

if __name__ == "__main__":
    main()
