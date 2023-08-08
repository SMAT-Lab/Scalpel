import numpy as np
import pandas as pd
from random import choices

pd.read_csv("test.csv")
np.array([1,2,3,4,5,6])
data = [41, 50, 29]
means = sorted(mean(choices(data, k=len(data))) for i in range(100))