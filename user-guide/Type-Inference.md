

Type inference module in Scalpel can identify type information for the usage context. As a dynamically type languages, the variabes' type are unknown until runtime, making it difficult to perform type checking. Though benefiting from the coding flexibility for rapid development, Python programs can miss the opportunity to separate data from behavior and detect bugs and errors at an early stage. 

Scalpel provides a module `scalpel.typeinfer` for automatic type inference to facilitate static analysis for Python programs.
`scalpel.typeinfer` takes a python file or the root folder of a whole package as input, and will output a dictionary of detailed type information for each variable, including function return values and function parameters.

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
The first parameter of `TypeInference` is the desired name for the inference analyzer, and the second one is the path to a python file or the root folder of a python package. After instantiating a `TypeInference` analyzer, invoke `infer_types()` method to start the inferring process. `get_types()` will return a list containing inferred type information of all variables.
The output is as follows. 
```python
[{'file': 'type_infer_example.py', 'line_number': 4, 'function': 'my_function', 'type': {'str'}},
 {'file': 'type_infer_example.py', 'line_number': 5, 'variable': 'x', 'function': 'my_function', 'type': 'str'}]
```
As shown in the output, the type of the function return value is also inferred, which is `str`.

\
The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Type Inference Example](../examples/type_infer_tutorial.py)

### APIs
[Please refer to the API documentation](https://smat-lab.github.io/Scalpel/scalpel/typeinfer.html)

### Reference
1. [typegen4py](https://github.com/typegen4py/typegen4py).
2. [Aggressive Type Inference](https://legacy.python.org/workshops/2000-01/proceedings/papers/aycock/aycock.html#:~:text=3%20Aggressive%20Type%20Inference,string%20if%20S3%20is%20executed.)
3. [mypy](https://mypy.readthedocs.io/en/stable/type_inference_and_annotations.html)
4. [Alias Analysis for Optimization of Dynamic Languages](https://www3.cs.stonybrook.edu/~tuncay/papers/GLSRT-DLS-10.pdf)
5. [NL2Type: Inferring JavaScript Function Types from Natural
Language Information](https://www.software-lab.org/publications/icse2019_NL2Type.pdf)
