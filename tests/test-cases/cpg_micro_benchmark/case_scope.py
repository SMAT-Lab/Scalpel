from flask import Flask, request
app = Flask(__name__)
code = request.args.get("code")
@app.route("/code-execution")
def code_execution():
    exec(code) # OK

code = ""
def code_execution2():
    exec(code) # OK