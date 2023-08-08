""" Script to test static as well as dynamic fully qualified name inference in Scalpel"""

from scalpel.fully_qualified_name_inference import FullyQualifiedNameInference

src = source = open("tests/test-cases/fully_qualified_name_inference/basics.py").read()

static_inference_actual = """
[{'call_name': 'pd.read_csv', 'line_no': 6, 'full_name': 'pandas.read_csv'}, {'call_name': 'np.array', 'line_no': 7, 'full_name': 'numpy.array'}]

"""
dynamic_inference_actual = """
[{'call_name': 'pd.read_csv', 'line_no': 6, 'full_name': 'pandas.io.parsers.readers.read_csv'}, {'call_name': 'np.array', 'line_no': 7, 'full_name': 'numpy.array'}]

"""

def assert_list_of_dictionaries_equal(list_1, list_2):
    """Asserts that two lists of dictionaries are equal.

    Args:
    list_1: The first list of dictionaries.
    list_2: The second list of dictionaries.

    Raises:
    AssertionError: If the two lists are not equal.
    """

    assert len(list_1) == len(list_2), "The lists must be the same length."
    for dict_1, dict_2 in zip(list_1, list_2):
        assert dict_1 == dict_2, "The dictionaries must be equal."
        

def test_static_inference():
    
    static_inference = FullyQualifiedNameInference(src = src, is_path= False, dynamic = False )
    assert_list_of_dictionaries_equal(static_inference , static_inference_actual)
    #assert static_inference == static_inference_actual

def test_dynamic_inference():
    
    dynamic_inference= FullyQualifiedNameInference(src = src, is_path= False, dynamic = True )
    assert_list_of_dictionaries_equal(dynamic_inference, dynamic_inference_actual)
    #assert dynamic_inference == dynamic_inference_actual

def main():
    test_static_inference()
    test_dynamic_inference()
    
if __name__ == '__main__':
    main()