from flask import Flask, request
app = Flask(__name__)

# case 1 - decorator
# Fail
code = request.args.get("code")

def a_dec_function(arg):
    def inner_func(func):
        def wrapper():
            exec(arg)
            func()
        return wrapper
    return inner_func


@a_dec_function("/code-execution")
def code_execution():
    pass

code_execution()



# case 2 - decorator
# Fail

def a_dec_function2(func):
    def wrapper(cmd):
        exec(cmd) # NOT OK
        func(cmd)
    return wrapper

@a_dec_function
def code_execution2(code):
    pass

code_execution2()



# case 3 - context manager

class HelloContextManager:
    def __init__(self,arg1):
        self.arg1=arg1

    def __enter__(self):
        exec(self.arg1)
        return "Hello, World!"
    def __exit__(self):
        print("Leaving the context...")


def code_execution3():
    code = request.args.get("code")
    with HelloContextManager(code) as c:
        print(c)


# case 4 - context manager

class HelloContextManager2:
    def __init__(self, arg1):
        self.arg1 = arg1

    def __enter__(self):
        return self.arg1

    def __exit__(self):
        print("Leaving the context...")


def code_execution4():
    code = request.args.get("code")
    with HelloContextManager2(code) as c:
        exec(c)


# case 5 - list comp

def code_execution5():
    lst1 = [request.args.get("code")]
    lst2 = [i for i in lst1]
    for i in lst2:
        exec(i)