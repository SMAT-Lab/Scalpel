#!/usr/bin/env python
# coding: utf-8
# In[1]:
from time import time
import warnings
warnings.filterwarnings('ignore')
# Import libraries to manipulate data
import numpy as np
import pandas as pd
pd.options.display.max_columns = 999
# Import libraries for visualization
# Matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# Seaborn, handy usage with pandas DataFrames
import seaborn as sns
# In[2]:
# Load from csv files
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
# Visualize head of DataFrame
train.head(5)
# In[3]:
print("Test data shape", test.shape)
print("Training data shape", train.shape)
train.dtypes
# In[4]:
print(train.isnull().values.any())
print(train.isna().values.any())
for element in list(train['TotalCharges']):
    try: float(element)
    except: print(list(element))
# In[5]:
train['SeniorCitizen'] = train['SeniorCitizen'].map(lambda x: 'No' if x==0 else 'Yes')
test['SeniorCitizen'] = test['SeniorCitizen'].map(lambda x: 'No' if x==0 else 'Yes')
train['TotalCharges'] = train['TotalCharges'].map(lambda x: 0. if x==' ' else float(x))
test['TotalCharges'] = test['TotalCharges'].map(lambda x: 0. if x==' ' else float(x))
# In[6]:
# There are 3 numerical features in the training data that can be summerized by .describe()
train.describe()
# In[7]:
for col in train.columns:
    print('Cardinality for %s: ' %(col), len(np.unique(train[col])))
# In[8]:
#Class imbalance
plt.figure(figsize=(15,6))
sns.countplot(x='Churn', data=train);
# In[9]:
low_card_features = [col for col in train.columns
                     if col not in ['tenure', 'MonthlyCharges', 'TotalCharges', 'customerID', 'Churn']]
for i in range(0,len(low_card_features)-1,2) :
    f, (ax1, ax2) = plt.subplots(1,2, figsize=(15,6))
    ax1.set_title(low_card_features[i])
    sns.countplot(x=low_card_features[i], data=train, hue='Churn', ax=ax1)
    ax2.set_title(low_card_features[i+1])
    sns.countplot(x=low_card_features[i+1], data=train, hue='Churn', ax=ax2)
    plt.show()
# In[10]:
plt.figure(figsize=(15,6))
plt.title('Tenure')
sns.countplot(x='tenure', data=train, hue='Churn');
# In[11]:
plt.figure(figsize=(15,6))
plt.title('Monthly Charges')
sns.boxplot(x=train['MonthlyCharges'],y=[""]*len(train),hue=train['Churn']);
# In[12]:
plt.figure(figsize=(15,6))
plt.title('Total Charges')
sns.boxplot(x=train['TotalCharges'],y=[""]*len(train),hue=train['Churn']);
# In[14]:
get_ipython().run_cell_magic('file', 'submissions/starting_kit/feature_extractor.py', "import pandas as pd\npd.options.mode.chained_assignment = None\nimport numpy as np \n\nclass FeatureExtractor():\n    \n    def __init__(self):\n        pass\n\n    def fit(self, X_df, y):\n        pass\n\n    def transform(self, X_df):\n        \n        X_tf = pd.DataFrame()\n        \n        # Change datatypes of the columns that we pointed out in the first section\n        X_df.loc[:,'SeniorCitizen'] = X_df['SeniorCitizen'].map(lambda x: 'No' if x==0 else 'Yes')\n        X_df.loc[:,'TotalCharges'] = X_df['TotalCharges'].map(lambda x: 0. if x==' ' else float(x))\n        \n        # For the first step, consider only the categorical features of the data\n        X_df_reduced = X_df.drop(['tenure', 'MonthlyCharges', 'TotalCharges','customerID'], axis=1)\n\n        # Perform one-hot encoding on the categorical variables\n        X_tf = pd.get_dummies(X_df_reduced)\n        \n        return X_tf")
# In[15]:
get_ipython().run_cell_magic('file', 'submissions/starting_kit/classifier.py', 'from sklearn.base import BaseEstimator\nfrom sklearn.ensemble import RandomForestClassifier\n\nclass Classifier(BaseEstimator):\n    \n    def __init__(self):\n        self.clf = RandomForestClassifier()\n        \n    def fit(self, X, y):\n        self.clf.fit(X, y)\n        \n    def predict(self, X):\n        return self.clf.predict(X)\n\n    def predict_proba(self, X):\n        return self.clf.predict_proba(X)')
# In[18]:
# %load submissions/starting_kit/classifier.py
# In[20]:
# %load submissions/starting_kit/feature_extractor.py
# In[24]:
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
# Separate data from labels
X_train = train.drop(['Churn'], axis=1)
Y_train = train['Churn']
# Split the training data for local testing
X_train,X_test_local,Y_train,Y_test_local = train_test_split(X_train,Y_train,test_size = 0.20) 
        
# Transform data into feature matrices
F = FeatureExtractor()
X_train = F.transform(X_train)
X_test_local = F.transform(X_test_local)
# Create classifier instance and train
clf = Classifier()
t0=time()
clf.fit(X_train,Y_train)
print('------------------ Training Done in %f s ------------------\nPrinting Score...' %(time()-t0))
# Run prediction on test data
y_pred = clf.predict(X_test_local)
# Visualize confusion matrix with seaborn heatmap
plt.figure(figsize=(10,6))
plt.title('confusion matrix')
cm = confusion_matrix(Y_test_local, y_pred)
g = sns.heatmap(cm,
            annot=True,
            fmt='d',
            cmap=sns.cubehelix_palette(8));
g.set_yticklabels(['Non-churner', 'Churner'], rotation=25)
g.set_xticklabels(['Non-churner', 'Churner'])
# Print classification report to have metrics on both classes
print(classification_report(Y_test_local, y_pred, target_names=['Non-churner', 'Churner']))
print('------------------ Visualizing confusion matrix ------------------')
# In[37]:
get_ipython().system('ramp_test_submission --quick-test')