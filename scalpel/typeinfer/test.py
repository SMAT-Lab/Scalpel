"""
Tomas Bolger 2021
Python 3.9
Unittests for base cases
"""

import unittest

from typeinfer import TypeInference


class BaseCaseTests(unittest.TestCase):

    def test_case_1(self):
        infferer = TypeInference(name='case1.py', entry_point='basecase/case1.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case1.py', 'line_number': 10, 'function': 'my_function', 'type': {'Dict[str, str]'}},
             {'file': 'case1.py', 'line_number': 14, 'variable': 'my_var', 'function': 'my_function',
              'type': 'Dict[str, str]'}]
        )

    def test_case_2(self):
        infferer = TypeInference(name='case2.py', entry_point='basecase/case2.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case2.py', 'line_number': 6, 'function': 'my_function', 'type': {'str'}}]
        )

    def test_case_3(self):
        infferer = TypeInference(name='case3.py', entry_point='basecase/case3.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case3.py', 'line_number': 8, 'function': 'my_function', 'type': {'str', 'int'}},
             {'file': 'case3.py', 'line_number': 8, 'parameter': 'my_bool', 'function': 'my_function', 'type': 'any'},
             {'file': 'case3.py', 'line_number': 10, 'variable': 'my_int', 'function': 'my_function', 'type': 'int'},
             {'file': 'case3.py', 'line_number': 13, 'variable': 'my_str', 'function': 'my_function', 'type': 'str'}]
        )

    def test_case_4(self):
        infferer = TypeInference(name='case4.py', entry_point='basecase/case4.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case4.py', 'line_number': 12, 'function': 'MyClass.get_hash', 'type': {'dict'}}]
        )

    def test_case_5(self):
        infferer = TypeInference(name='case5.py', entry_point='basecase/case5.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case5.py', 'line_number': 9, 'function': 'my_function', 'type': {'int'}},
             {'file': 'case5.py', 'line_number': 10, 'variable': 'x', 'function': 'my_function', 'type': 'int'},
             {'file': 'case5.py', 'line_number': 11, 'variable': 'y', 'function': 'my_function', 'type': 'int'},
             {'file': 'case5.py', 'line_number': 12, 'variable': 'z', 'function': 'my_function', 'type': 'int'}]
        )

    def test_case_6(self):
        infferer = TypeInference(name='case6.py', entry_point='basecase/case6.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case6.py', 'line_number': 9, 'function': 'my_function', 'type': {'str'}},
             {'file': 'case6.py', 'line_number': 10, 'variable': 'x', 'function': 'my_function', 'type': 'int'},
             {'file': 'case6.py', 'line_number': 11, 'variable': 'y', 'function': 'my_function', 'type': 'int'},
             {'file': 'case6.py', 'line_number': 12, 'variable': 'z', 'function': 'my_function', 'type': 'int'}]
        )

    def test_case_7(self):
        infferer = TypeInference(name='case7.py', entry_point='basecase/case7.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            []
        )

    def test_case_8(self):
        infferer = TypeInference(name='case8.py', entry_point='basecase/case8.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case8.py', 'line_number': 7, 'function': 'my_function', 'type': {'callable'}},
             {'file': 'case8.py', 'line_number': 8, 'function': 'my_inner_function', 'type': {'int'}}]
        )

    def test_case_9(self):
        infferer = TypeInference(name='case9.py', entry_point='basecase/case9.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case9.py', 'line_number': 13, 'function': 'ParentClass.my_function', 'type': {'list'}},
             {'file': 'case9.py', 'line_number': 21, 'function': 'ChildClass.my_function', 'type': {'list'}}]
        )

    def test_case_10(self):
        infferer = TypeInference(name='case10.py', entry_point='basecase/case10.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case10.py', 'line_number': 10, 'function': 'my_function', 'type': {'defaultdict'}},
             {'file': 'case10.py', 'line_number': 11, 'variable': 'my_default_dict', 'function': 'my_function',
              'type': 'defaultdict'}]
        )

    def test_case_11(self):
        infferer = TypeInference(name='case11.py', entry_point='basecase/case11.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case11.py', 'line_number': 7, 'function': 'my_function', 'type': {'int', 'str'}},
             {'file': 'case11.py', 'line_number': 7, 'parameter': 'my_bool', 'function': 'my_function', 'type': 'any'},
             {'file': 'case11.py', 'line_number': 9, 'variable': 'x', 'function': 'my_function', 'type': 'int'},
             {'file': 'case11.py', 'line_number': 11, 'variable': 'x', 'function': 'my_function', 'type': 'str'}]
        )

    def test_case_12(self):
        infferer = TypeInference(name='case12.py', entry_point='basecase/case12.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case12.py', 'line_number': 1, 'function': 'my_function', 'type': {'int'}},
             {'file': 'case12.py', 'line_number': 1, 'parameter': 'my_val', 'function': 'my_function', 'type': 'int'},
             {'file': 'case12.py', 'line_number': 2, 'variable': 'x', 'function': 'my_function', 'type': 'int'},
             {'file': 'case12.py', 'line_number': 3, 'variable': 'y', 'function': 'my_function', 'type': 'int'},
             {'file': 'case12.py', 'line_number': 4, 'variable': 'g', 'function': 'my_function', 'type': 'int'},
             {'file': 'case12.py', 'line_number': 5, 'variable': 'z', 'function': 'my_function', 'type': 'int'}]
        )


if __name__ == '__main__':
    unittest.main()
