# Returning defined variable

# EXPECTED OUTPUT:
# case1.py: my_var -> Dict[str, str]
# case1.py: my_function() -> Dict[str, str]

def my_function():
    my_var = {"hello": "world"}
    return my_var
