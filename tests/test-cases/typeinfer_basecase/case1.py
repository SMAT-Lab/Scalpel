# Returning defined variable

# EXPECTED OUTPUT:
# case1.py: my_var -> Dict[str, str]
# case1.py: my_function() -> Dict[str, str]

from collections import defaultdict


def my_function():
    """
    Function comment
    """
    my_var = {"hello": "world"}
    return my_var
