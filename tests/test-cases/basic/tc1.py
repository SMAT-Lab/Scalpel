class FakeClass:
    def fake_function(self,a,b):
        a=a+1
        return a+b
fake_class = FakeClass()
fake_class.fake_function(1,2)