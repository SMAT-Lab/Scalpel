import unittest, ast
from _ast import AST, Assign, SetComp
import astor
from ..scalpel.core.base.stmt import AssignStmt, SStmt
# from duc import _ContainerRelationshipVisitor

class TestStmtMethods(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_AssignStmt_get_clauses(self):
        assign_node = ast.parse("a = b = 1").body[0]
        print(type(assign_node))
        self.assertIsInstance(assign_node, ast.stmt)
        sstmt = SStmt(assign_node)
        print(sstmt.get_clauses())
        # self.assertEqual(sstmt.get_clauses().value, 1)
        

if __name__ == '__main__':
    unittest.main()
