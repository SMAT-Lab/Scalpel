"""
Script to test static as well as dynamic fully qualified name inference in Scalpel.
"""

from pathlib import Path

from test_fqn_actual_data import GROUND_TRUTH

from scalpel.fqn import FullyQualifiedNameInference as FQNInference

SCRIPT_DIR = Path(__file__).parent
TEST_CASE_DIR = SCRIPT_DIR / "test-cases/fully_qualified_name_inference"
# run pip install pandas numpy keras seaborn matplotlib to pass "external_lib_test"
TEST_CASES = ["case1", "case2", "case3", "external_lib_test"]


def main():
    """
    Main test runner.
    """
    for test_case in TEST_CASES:
        static_actual = GROUND_TRUTH[f"{test_case}_static"]
        dynamic_actual = GROUND_TRUTH[f"{test_case}_dynamic"]

        static_inference = FQNInference(
            file_path=TEST_CASE_DIR / (test_case + ".py"), dynamic=False
        ).infer()
        assert sorted(static_inference) == sorted(static_actual)

        dynamic_inference = FQNInference(
            file_path=TEST_CASE_DIR / (test_case + ".py"), dynamic=True
        ).infer()
        assert sorted(dynamic_inference) == sorted(dynamic_actual)


if __name__ == "__main__":
    main()
