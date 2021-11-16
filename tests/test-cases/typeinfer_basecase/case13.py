# Chained function calls

# EXPECTED OUTPUT:
# case13.py: first_function -> str
# case13.py: second_function -> str
# case13.py: third_function -> str

def first_function():
    return second_function()


def second_function():
    return "Hello World!"


def third_function():
    return second_function()
