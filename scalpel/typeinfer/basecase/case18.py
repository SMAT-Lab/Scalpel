class MyParentClass:
    def __init__(self):
        self.parent_attribute = ["Hello", "World", "!"]

    def my_function(self):
        return " ".join(self.parent_attribute)


class ChildClass(MyParentClass):

    def my_function(self):
        return super().parent_attribute
