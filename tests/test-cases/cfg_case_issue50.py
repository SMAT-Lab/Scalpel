class A:
    def func_a(self):
        print("whatsup")

class B:
    def func_b(self):
        print("hello")

class A(A):
    def __init__(self, count):
        self.count = count
    def fib(self):
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

a = A(1)
fib_gen = a.fib()
for _ in range(10):
    next(fib_gen)