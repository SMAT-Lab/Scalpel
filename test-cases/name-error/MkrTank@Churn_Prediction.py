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
# Seaborn, handy usage with pandas DataFrames
import seaborn as sns
# Load from csv files
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
# Visualize head of DataFrame
train.head(5)
print("Test data shape", test.shape)
print("Training data shape", train.shape)
train.dtypes
print(train.isnull().values.any())
print(train.isna().values.any())
for element in list(train['TotalCharges']):
    try: float(element)
    except: print(list(element))
train['SeniorCitizen'] = train['SeniorCitizen'].map(lambda x: 'No' if x==0 else 'Yes')
test['SeniorCitizen'] = test['SeniorCitizen'].map(lambda x: 'No' if x==0 else 'Yes')
train['TotalCharges'] = train['TotalCharges'].map(lambda x: 0. if x==' ' else float(x))
test['TotalCharges'] = test['TotalCharges'].map(lambda x: 0. if x==' ' else float(x))
# There are 3 numerical features in the training data that can be summerized by .describe()
train.describe()
for col in train.columns:
    print('Cardinality for %s: ' %(col), len(np.unique(train[col])))
#Class imbalance
plt.figure(figsize=(15,6))
sns.countplot(x='Churn', data=train);
low_card_features = [col for col in train.columns
                     if col not in ['tenure', 'MonthlyCharges', 'TotalCharges', 'customerID', 'Churn']]
for i in range(0,len(low_card_features)-1,2) :
    f, (ax1, ax2) = plt.subplots(1,2, figsize=(15,6))
    ax1.set_title(low_card_features[i])
    sns.countplot(x=low_card_features[i], data=train, hue='Churn', ax=ax1)
    ax2.set_title(low_card_features[i+1])
    sns.countplot(x=low_card_features[i+1], data=train, hue='Churn', ax=ax2)
    plt.show()
plt.figure(figsize=(15,6))
plt.title('Tenure')
sns.countplot(x='tenure', data=train, hue='Churn');
plt.figure(figsize=(15,6))
plt.title('Monthly Charges')
sns.boxplot(x=train['MonthlyCharges'],y=[""]*len(train),hue=train['Churn']);
plt.figure(figsize=(15,6))
plt.title('Total Charges')
sns.boxplot(x=train['TotalCharges'],y=[""]*len(train),hue=train['Churn']);
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np 
class FeatureExtractor():
    
    def __init__(self):
        pass
    def fit(self, X_df, y):
        pass
    def transform(self, X_df):
        
        X_tf = pd.DataFrame()
        
        # Change datatypes of the columns that we pointed out in the first section
        X_df.loc[:,'SeniorCitizen'] = X_df['SeniorCitizen'].map(lambda x: 'No' if x==0 else 'Yes')
        X_df.loc[:,'TotalCharges'] = X_df['TotalCharges'].map(lambda x: 0. if x==' ' else float(x))
        
        # For the first step, consider only the categorical features of the data
        X_df_reduced = X_df.drop(['tenure', 'MonthlyCharges', 'TotalCharges','customerID'], axis=1)
        # Perform one-hot encoding on the categorical variables
        X_tf = pd.get_dummies(X_df_reduced)
        
        return X_tf
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier
class Classifier(BaseEstimator):
    
    def __init__(self):
        self.clf = RandomForestClassifier()
        
    def fit(self, X, y):
        self.clf.fit(X, y)
        
    def predict(self, X):
        return self.clf.predict(X)
    def predict_proba(self, X):
        return self.clf.predict_proba(X)
# %load submissions/starting_kit/classifier.py
# %load submissions/starting_kit/feature_extractor.py
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