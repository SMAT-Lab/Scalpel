"""
For some reason, we give User() explicitly to my_func_lower but it is not picked up?
"""


def my_func_main():
    x = User()
    y = User()
    my_func_lower(x, y)


def my_func_lower(user_1, user_2):
    user_1.misc_calc()
    user_2.misc_calc()


class User:
    @staticmethod
    def misc_calc():
        return 10

