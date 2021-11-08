# Binary operation in function return with imported callable

# EXPECTED OUTPUT:
# case14.py: x -> str
# case15.py: my_function -> str


from os import getcwd


def my_function():
    x = "Current working directory: "
    return x + getcwd()
