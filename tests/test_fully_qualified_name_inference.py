""" Script to test static as well as dynamic fully qualified name inference in Scalpel"""

from scalpel import fully_qualified_name_inference as fni
import test_name_infer_actual_data as actual

source_test_basics = open("tests/test-cases/fully_qualified_name_inference/basics.py").read()
source_test_nested_func_calls = open("tests/test-cases/fully_qualified_name_inference/nested_func_calls.py").read()
source_test_func_inside_func_calls = open("tests/test-cases/fully_qualified_name_inference/func_inside_func_calls.py").read()


# def assert_list_of_dictionaries_equal(list_1, list_2):
#     """Asserts that two lists of dictionaries are equal.

#     Args:
#     list_1: The first list of dictionaries.
#     list_2: The second list of dictionaries.

#     Raises:
#     AssertionError: If the two lists are not equal.
#     """

#     assert len(list_1) == len(list_2), "The lists must be the same length."
#     for dict_1, dict_2 in zip(list_1, list_2):
#         assert dict_1 == dict_2, "The dictionaries must be equal."

def test_basics():
    
    static_inference_actual = actual.actual_data_test_basics_static()
    dynamic_inference_actual = actual.actual_data_test_basics_dynamic()
    
    static_inference = fni.FullyQualifiedNameInference(src = source_test_basics, is_path= False, dynamic = False )
    #assert_list_of_dictionaries_equal(static_inference , static_inference_actual)
    assert static_inference == static_inference_actual
    
    dynamic_inference= fni.FullyQualifiedNameInference(src = source_test_basics, is_path= False, dynamic = True )
    #assert_list_of_dictionaries_equal(dynamic_inference, dynamic_inference_actual)
    assert dynamic_inference == dynamic_inference_actual

def test_nested_func_calls():
    inference_actual = actual.actual_data_test_nested_func_calls_static()
    inference = fni.FullyQualifiedNameInference(src = source_test_nested_func_calls, is_path= False, dynamic = False)
    assert inference == inference_actual
    
def test_func_inside_func_calls():
    inference_actual = actual.actual_data_test_func_inside_func_calls_static()
    inference = fni.FullyQualifiedNameInference(src = source_test_func_inside_func_calls, is_path= False, dynamic = False)
    assert inference == inference_actual


def main():
    test_basics()
    test_nested_func_calls()
    test_func_inside_func_calls()
    
if __name__ == '__main__':
    main()