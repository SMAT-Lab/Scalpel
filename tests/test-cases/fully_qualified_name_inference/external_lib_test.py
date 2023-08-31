import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from keras.models import Sequential

train_orj = pd.read_csv("../input/train.csv", header=0)

plt.figure(figsize=(10, 5))
sns.countplot(train_orj.Age, palette="icefire")

model = Sequential()

iris_dataset = sns.load_dataset("iris")
