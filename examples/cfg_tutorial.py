from scalpel.cfg import CFGBuilder

def main():
    cfg = CFGBuilder().build_from_file('example.py', './cfg_example_case.py')
    cfg.build_visual('pdf')
    for block in cfg:
        calls = block.get_calls()
        print(calls)
    example_block = cfg.get_all_blocks()[-1]
    a_value = cfg.backward(example_block,'a',[],[])
    print(a_value)
if __name__ == "__main__":
    main()
