'''
From pytest_outcomes.py
'''
def __repr__(self) -> str:
    if self.msg is not None:
        return self.msg
    return f"<{self.__class__.__name__} instance>"