class MyParentClass:
    def __init__(self):
        self.attribute = ["Hello", "World", "!"]

    def my_function(self):
        return " ".join(self.attribute)


class ChildClass(MyParentClass):

    def my_function(self):
        return super().attribute
