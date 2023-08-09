import os

from scalpel.core.mnode import MNode

source = """
import numpy as np
import pandas as pd
from random import choices

pd.read_csv("test.csv")
np.array([1,2,3,4,5,6])
data = [41, 50, 29]
means = sorted(mean(choices(data, k=len(data))) for i in range(100))

"""


def main():
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
            dotted_parts = [import_dict[dotted_parts[0]]] + dotted_parts[1:]
            call_name = ".".join(dotted_parts)
        print(call_name)


if __name__ == "__main__":
    main()
