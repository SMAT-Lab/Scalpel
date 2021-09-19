# Imported data structure

# EXPECTED OUTPUT:
# case10.py: my_default_dict -> defaultdict
# case10.py: my_function-> defaultdict

from os import getcwd


def my_function():
    my_default_dict = getcwd()
    return my_default_dict
