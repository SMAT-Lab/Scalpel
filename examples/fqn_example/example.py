from random import choices

import pandas as pd
import seaborn as sns

data = [41, 50, 29]
random_choices = choices(data, k=len(data))
print(random_choices)

iris_dataset = sns.load_dataset("iris")
sns.countplot(X, palette="icefire")

train_orj = pd.read_csv("train.csv", header=0)
