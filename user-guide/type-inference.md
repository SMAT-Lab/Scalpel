
## Type Inference
`scalpel.typeinfer` module can used to infer the types of the variables in a python program, which is super useful in many static analysis tasks. `scalpel.type_inference` takes a python module or the root folder of a whole package as input, and will output a dictionary of detailed type information for each variable, including function return values and function parameters.



### How to use Type Inference
Below is the demo input python program we will be using. The piece of code returns current working directory and is named "type_infer_example.py".
```python
from os import getcwd

def my_function():
    x = "Current working directory: "
    return x + getcwd()
```
To infer the types of the variables, we will use `TypeInference` class in `scalpel.typeinfer`.
```python
from scalpel.typeinfer.typeinfer import TypeInference

inferer = TypeInference(name='type_infer_example.py', entry_point='type_infer_example.py')
inferer.infer_types()
inferred = inferer.get_types()
```
The first parameter of `TypeInference` is the desired name for the inference analyzer, and the second one is the path to a python file or a root folder of a python package. After instantiating a `TypeInference` analyzer, invoke `infer_types()` method to start the inferring process. `get_types()` will return a list containing inferred type information of all variables.
The output is as follows. 
```python
[{'file': 'case15.py', 'line_number': 11, 'function': 'my_function', 'type': {'str'}},
 {'file': 'case15.py', 'line_number': 12, 'variable': 'x', 'function': 'my_function', 'type': 'str'}]
```
The function return value is also inferred.

\
The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Type Inference Example](../examples/type_infer_tutorial.py)

### APIs
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)

### Reference
1. [typegen4py](https://github.com/typegen4py/typegen4py).
2. 
