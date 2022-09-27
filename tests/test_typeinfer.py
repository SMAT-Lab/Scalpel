"""
Tomas Bolger 2021
Python 3.9
Unittests for base cases
"""

import unittest
import os
from scalpel.typeinfer.typeinfer import TypeInference, TypeInferenceJedi
from collections import OrderedDict
import test_typeinfer_actual_data as ActualData

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]


class DefaultTypeInferer(unittest.TestCase):
    def test_case_1(self):
        infferer = TypeInference(
            name="case1.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case1.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_1()

    def test_case_2(self):
        infferer = TypeInference(
            name="case2.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case2.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_2()

    def test_case_3(self):
        infferer = TypeInference(
            name="case3.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case3.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_3()

    def test_case_4(self):
        infferer = TypeInference(
            name="case4.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case4.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_4()

    def test_case_5(self):
        infferer = TypeInference(
            name="case5.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case5.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_5()

    def test_case_6(self):
        infferer = TypeInference(
            name="case6.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case6.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_6()

    def test_case_7(self):
        infferer = TypeInference(
            name="case7.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case7.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert inferred == []

    def test_case_8(self):
        infferer = TypeInference(
            name="case8.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case8.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_8()

    def test_case_9(self):
        infferer = TypeInference(
            name="case9.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case9.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_9()

    def test_case_10(self):
        infferer = TypeInference(
            name="case10.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case10.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_10()
        )

    def test_case_11(self):
        infferer = TypeInference(
            name="case11.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case11.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_11()
        )

    def test_case_12(self):
        infferer = TypeInference(
            name="case12.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case12.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_12()
        )

    def test_case_13(self):
        infferer = TypeInference(
            name="case13.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case13.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_13()
        )

    def test_case_14(self):
        infferer = TypeInference(
            name="case14.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case14.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_14()
        )

    def test_case_15(self):
        infferer = TypeInference(
            name="case15.py",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case15.py",
        )
        infferer.infer_types()
        inferred = infferer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_15()
        )

    def test_case_16(self):
        inferrer = TypeInference(
            name="case16",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case16",
        )
        inferrer.infer_types()
        inferred = inferrer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_16()
        )

    def test_case_17(self):
        inferrer = TypeInference(
            name="case17",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case17.py",
        )
        inferrer.infer_types()
        inferred = inferrer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_17()
        )

    def test_case_18(self):
        inferrer = TypeInference(
            name="case18",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case18.py",
        )
        inferrer.infer_types()
        inferred = inferrer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_18()
        )

    def test_case_19(self):
        # TODO: Resolve this test case
        inferrer = TypeInference(
            name="case18",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case19.py",
        )
        inferrer.infer_types()
        inferred = inferrer.get_types()
        # self.assertEqual(inferred, [])

    def test_case_20(self):
        inferrer = TypeInference(
            name="case20",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case20.py",
        )
        inferrer.infer_types()
        inferred = inferrer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_20()
        )

    def test_case_23(self):
        inferrer = TypeInference(
            name="case23",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case23.py",
        )
        inferrer.infer_types()
        inferred = inferrer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_23()
        )

    def test_case_24(self):
        inferrer = TypeInference(
            name="case24",
            entry_point=current_directory + "/test-cases/typeinfer_basecase/case24.py",
        )
        inferrer.infer_types()
        inferred = inferrer.get_types()
        assert (
            sorted(inferred, key=lambda x: str(x)) == ActualData.actual_data_case_24()
        )


if __name__ == "__main__":
    unittest.main()
