
## Middle Level Modules
The middle level modules of Scapel operates on the scope of the whole program (inter-procedural)

### Parse Function/Class Definitions
Introduction to Import Graph module...\
How to use Import Graph\
...

### API Name Qualifying
The known qualified name is a dotted string that represent the path from top-level module down to the object iteself.  The name format is defined in [PEP 3155](https://www.python.org/dev/peps/pep-3155/). Obtainning the qualified API names are very import to API anaysis as the same function calls can appear in different source code with different names. Without qualifying them first,  it is hard to perform even basic statisitcal anaysis. 

In this module, we show examples to use the functionalities of  call name extraction and import statement parsing to restore the call names. We implement the algorithm proposed by [1] that parsing all import statements to obtain a dictionary data structure for mapping the imported aliases and the API occurrents in the source code. 

The code to be analyzed:

```python
source = """
import numpy as np
import pandas as pd
from random import choices

pd.read_csv("test.csv")
np.array([1,2,3,4,5,6])
data = [41, 50, 29]
means = sorted(mean(choices(data, k=len(data))) for i in range(100))

"""
```

Example code:


```python
mnode = MNode("local")
mnode.source = source
mnode.gen_ast()
# parse all function calls
func_calls = mnode.parse_func_calls()
# obtain the imported name information
import_dict = mnode.parse_import_stmts()
for call_info in func_calls:
    call_name = call_info["name"]
    dotted_parts = call_name.split(".")
    # if this function calls is from a imported module
    if dotted_parts[0] in import_dict:
        dotted_parts = [import_dict[dotted_parts[0]]]+dotted_parts[1:]
        call_name = ".".join(dotted_parts)
    print(call_name)

```

The execution results of this example should be as :
```
pandas.read_csv
numpy.array
sorted
mean
len
range
```
As we can see, the function call `np.array`, `pd.read_csv` are recovered to `numpy.array` and `pandas.read_csv` respectively while the rest of function calls have their own name directly outputed. 


The full code of this example can be found in [API_name_qualifying.py](../examples/API_name_qualifying.py)

### References
[Jiawei Wang, Li Li, Kui Liu, Haipeng Cai, Exploring How Deprecated Python Library APIs are (Not) Handled, The 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE 2020)](https://lilicoding.github.io/papers/wang2020exploring.pdf)
