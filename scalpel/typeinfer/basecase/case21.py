# func_2 has same return type as my_parameter

# EXPECTED OUTPUT:
# case21.py: x -> str

def func_3():
    func_1("test", 20)
    func_1(func_2(), func_4())
    return True


def func_1(my_parameter, parameter_two):
    # do stuff
    result = my_parameter
    thing = parameter_two
    return result, thing


def func_2():
    return "test"


def func_4():
    return 30
