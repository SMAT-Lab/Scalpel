class test_obj:
    def __init__(self):
        self.func_2 = func_2


def func_3():
    func_1().func_2()


def func_2():
    return "test"


def func_1():
    my_obj = test_obj()
    return my_obj


