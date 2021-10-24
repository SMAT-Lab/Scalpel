# Class method return

# EXPECTED OUTPUT:
# case4.py: MyClass.hash -> dict
# case4.py: MyClass.get_hash() -> {}

class MyClass:

    def __init__(self):
        self.hash = {}

    def get_hash(self):
        return self.hash
