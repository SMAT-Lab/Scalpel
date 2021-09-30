def my_func_main():
    my_func_lower(User(), User())


def my_func_lower(user_1, user_2):
    user_1.misc_calc()
    user_2.misc_calc()


class User:
    @staticmethod
    def misc_calc():
        return 10

