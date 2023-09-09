from flask import Flask, request
app = Flask(__name__)

@app.route("/code-execution")
def code_execution():
    code = request.args.get("code")
    v1 = "cmd:"
    s = func2(code,v1)
    exec(s) # NOT OK


def func2(x, y):
    a = x + y
    return a


def code_execution2():
    code = "nothing"
    v1 = "cmd:"
    s = func2(code,v1)
    exec(s)  # OK