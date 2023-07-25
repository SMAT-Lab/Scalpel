""" Script to test static as well as dynamic fully qualified name inference in Scalpel"""

from scalpel.fully_qualified_name_inference import FullyQualifiedNameInference

src = """
import numpy as np
import pandas as pd
from random import choices

pd.read_csv("test.csv")
np.array([1,2,3,4,5,6])
data = [41, 50, 29]
means = sorted(mean(choices(data, k=len(data))) for i in range(100))
"""

static_inference_actual = """
"""
dynamic_inference_actual = """
"""

def test_static_inference():
    
    static_inference = FullyQualifiedNameInference(src = src, is_path= False, dynamic = False )
    assert static_inference == static_inference_actual

def test_dynamic_inference():
    
    dynamic_inference= FullyQualifiedNameInference(src = src, is_path= False, dynamic = True )
    assert dynamic_inference == dynamic_inference_actual

def main():
    test_static_inference()
    test_dynamic_inference()
    
if __name__ == '__main__':
    main()