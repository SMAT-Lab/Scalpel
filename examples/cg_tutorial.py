from scalpel.pycg.pycg import CallGraphGenerator

cg_generator = CallGraphGenerator(["./cg_example_pkg/main.py"], "cg_example_pkg")
cg_generator.analyze()
cg = cg_generator.output