from scalpel.cfg import CFGBuilder

code_str="""
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
    cfg = CFGBuilder().build_from_src('example.py', code_str)
    cfg.build_visual('pdf')
    for block in cfg:
        calls = block.get_calls()
        print(calls)
    example_block = cfg.get_all_blocks()[-1]
    a_value = cfg.backward(example_block,'a',[],[])
    print(a_value)


if __name__ == "__main__":
    main()
