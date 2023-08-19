from flask import Flask, request
app = Flask(__name__)

class A:
    def __init__(self):
        self.a = ""
        self.b = ""

class B:
    b = request.args.get("code")
    def __init__(self,a,b):
        self.a = a
        # self.b = b

    def get_a(self):
        return self.a

@app.route("/code-execution")
def code_execution():
    code = request.args.get("code")
    # case 1 - dictionary
    dic = {}
    for i in range(10):
        dic[i] = request.args.get("code")

    dic["code"] = request.args.get("code")
    exec(dic[1])            # NOT OK
    exec(dic["code"])       # NOT OK
    exec(dic["randomstr"])  # OK

    # case 2 - normal object
    a = A()
    a.a = code
    v1 = "cmd:"
    s1 = func2(a.a,v1)
    exec(s1) # NOT OK
    s2 = func2(a.b, v1)
    exec(s2)  # OK


# case 3 - normal object
def code_execution2():
    code = request.args.get("code")
    a = B(code,"")
    v1 = "cmd:"
    s1 = func2(a.a,v1)
    exec(s1) # NOT OK
    s2 = func2(a.b, v1)
    exec(s2)  # NOT OK
    exec(a.get_a())  # NOT OK

def func2(x, y):
    a = x + y
    return a


# case 4 - list
def code_execution3():
    lst = []
    for i in range(10):
        lst[i] = request.args.get("code")

    exec(lst[1])

# case 5 - set
def code_execution4():
    tpl = (request.args.get("code"), "")

    exec(tpl[0])  # NOT OK
    exec(tpl[1])  # OK

# case 6 - For loop
def code_execution5():
    lst = [request.args.get("code")]
    for i in lst:
       exec(i)  # NOT OK