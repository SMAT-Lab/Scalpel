# Variable assigned different types in conditional block

# EXPECTED OUTPUT:
# case11.py: x -> Union[int, str]
# case11.py: my_function -> Union[int, str]

def my_function(my_bool):
    if my_bool:
        x = 5
    else:
        x = "Hello World!"
    return x
