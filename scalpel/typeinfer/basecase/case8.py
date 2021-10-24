# Callable return

# EXPECTED OUTPUT:
# case8.py: my_function.my_inner_function() -> int
# case8.py: my_function() -> callable

def my_function():
    def my_inner_function():
        return 5

    return my_inner_function
