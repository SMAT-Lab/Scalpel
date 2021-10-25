# Function parameter involved in a binary operation

# EXPECTED OUTPUT:
# case12.py: my_val -> int
# case12.py: x -> int
# case12.py: y -> int
# case12.py: g -> int
# case12.py: z -> int
# case12.py: my_function -> int


def my_function(my_val):
    x = 5
    y = 10
    g = 10
    z = x + y + g + my_val
    return z
