from scalpel.pycg.pycg import CallGraphGenerator
source = """
from .sub_folder1.module1 import Module1
from .sub_folder1.module2 import Module2

<<<<<<< HEAD
module1 = Module1()
do_add = module1.add(1,1)
module2 = Module2()
do_minus = module2.minus(1,1)

"""
cg_generator = CallGraphGenerator(["./cg_example_pkg/main.py"], "cg_example_pkg")
cg_generator.analyze()
cg = cg_generator.output
