# Rewriter

The objective of  rewriting module of Scalple is to provide APIs that allow users to rewrite their code implenmentation. This can be
for code desugaring (removing code sugar usages), testing and code instrumentation for various purpose. Code rewriting can bring great benefits such as API extraction and dynamic testing.


## How to use Rewriter
Right now, Scalple offers code rewriting at statement level. Users can implement their own rewrite rules and pass it to the Rewriter API. We will use the following example to show the usages. 

The demo input python program we will be using is as follows.
```python
src = """
a = list()
b = dict()
"""
```
Our aim is to rewrite the above code snippet to the following one:

```python
expected_src = """
a = []
b = {}
"""
```

We will firstly implement the rewrite rules, that for any given assignment statements, if there assigned values are dictionary or list function calls, then use the initalization syntax instead of function calls. We can define the rules as:

```python
def rewrite_rules(node)->list:
    if  isinstance(node, ast.Assign):
      if isinstance(node.value, ast.Call) and hasattr(node.value.func, "id"):
          if node.value.func.id == "list":
              new_assign_value = ast.List(elts=[], ctx=ast.Load())
              new_stmt = ast.Assign(node.targets, new_assign_value)
              return [new_stmt]
          if node.value.func.id == "dict":
              new_assign_value = ast.Dict(keys=[], values=[])
              new_stmt = ast.Assign(node.targets, new_assign_value)
              return [new_stmt]   
```
Please note that the in the rule function, you will need to create new statements for each of your rule (see how the `new_stmt` variable is formed). Finally, we can pass the rule funciton to the rewrite engine:

```python
rewriter = Rewriter()
new_src = rewriter.rewrite(src, rule_func = rewrite_rules)
print(new_src)
```

The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Rewriter Example](https://github.com/SMAT-Lab/Scalpel/blob/scalpel-dev/examples/rewriter_example.py)

## APIs
Please refer to the API documentation: {py:mod}`scalpel.rewriter`

## Reference
