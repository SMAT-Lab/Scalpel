# Mutliple return paths

# EXPECTED OUTPUT:
# case3.py: my_int -> int
# case3.py: my_str -> str
# case3.py: my_function() -> Union[int, str]

def my_function(my_bool):
    if my_bool:
        my_int = 200
        return my_int
    else:
        my_str = "This is a string!"
        return my_str
