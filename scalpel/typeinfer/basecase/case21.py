# func_2 has same return type as my_parameter

# EXPECTED OUTPUT:
# case21.py: x -> str

def func_3():
    func_1(20)
    func_1(func_2())
    return True


def func_1(my_parameter):
    # do stuff
    result = my_parameter
    return result


def func_2():
    return 20




