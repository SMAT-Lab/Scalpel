"""
Script to test static as well as dynamic fully qualified name inference in Scalpel.
"""

from pathlib import Path

import test_name_infer_actual_data as actual_data

from scalpel.fqn import FullyQualifiedNameInference as FQNInference

SCRIPT_DIR = Path(__file__).parent

SOURCE_TEST_BASIC = SCRIPT_DIR / "test-cases/fully_qualified_name_inference/basics.py"
SOURCE_TEST_NESTED_FUNC_CALLS = (
    SCRIPT_DIR / "test-cases/fully_qualified_name_inference/nested_func_calls.py"
)
SOURCE_TEST_FUNC_INSIDE_FUNC = (
    SCRIPT_DIR / "test-cases/fully_qualified_name_inference/func_inside_func_calls.py"
)


def test_basics():
    """
    Test basic FQN inference.
    """
    static_actual = actual_data.actual_data_test_basics_static()
    dynamic_actual = actual_data.actual_data_test_basics_dynamic()

    static_inference = FQNInference(file_path=SOURCE_TEST_BASIC, dynamic=False).infer()
    assert sorted(static_inference) == sorted(static_actual)

    dynamic_inference = FQNInference(file_path=SOURCE_TEST_BASIC, dynamic=True).infer()
    assert sorted(dynamic_inference) == sorted(dynamic_actual)


def test_nested_func_calls():
    """
    Test FQN inference for nested function calls.
    """
    actual = actual_data.actual_data_test_nested_func_calls_static()
    inference = FQNInference(
        file_path=SOURCE_TEST_NESTED_FUNC_CALLS, dynamic=False
    ).infer()
    assert inference == actual


def test_func_inside_func_calls():
    actual = actual_data.actual_data_test_func_inside_func_calls_static()
    inference = FQNInference(
        file_path=SOURCE_TEST_FUNC_INSIDE_FUNC, dynamic=False
    ).infer()
    assert inference == actual


def main():
    """
    Main test runner.
    """
    test_basics()
    test_nested_func_calls()
    test_func_inside_func_calls()


if __name__ == "__main__":
    main()
