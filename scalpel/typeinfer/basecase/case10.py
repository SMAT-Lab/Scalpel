# Local import

# EXPECTED OUTPUT:
# case10.py: child_class -> ChildClass
# case10.py: my_function-> list

from case9 import ChildClass


def my_function():
    child_class = ChildClass()
    return child_class.my_function()
