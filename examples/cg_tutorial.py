from scalpel.pycg.pycg import CallGraphGenerator

cg_generator = CallGraphGenerator(["main.py"], "example_pkg")
cg_generator.analyze()
cg = cg_generator.output