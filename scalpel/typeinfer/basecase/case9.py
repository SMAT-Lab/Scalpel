# Inheriting from parent class

# EXPECTED OUTPUT:
# case9.py: ParentClass.my_function() -> list
# case9.py: ChildClass.my_function() -> list


class ParentClass:

    def __init__(self):
        pass

    def my_function(self):
        return [1, 2, 3, 4, 5]


class ChildClass(ParentClass):
    def __init__(self):
        super().__init__()

    def my_function(self):
        return super().my_function()
