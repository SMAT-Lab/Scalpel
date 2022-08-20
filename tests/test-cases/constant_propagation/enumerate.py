import numpy as np
from sklearn.linear_model import LogisticRegression

range = np.geomspace(start=1e-7, stop=1e7)

for count, value in enumerate(range):
    logistic_reg = LogisticRegression(penalty='l2', solver='liblinear', C=value) 
