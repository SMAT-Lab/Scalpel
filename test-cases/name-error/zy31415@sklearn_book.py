import pandas as pd
import seaborn as sns
import numpy as np
# To plot pretty figures
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
from sklearn.model_selection import train_test_split
# Stratified sampling
housing["income_cat"] = np.ceil(housing["median_income"] / 1.5)
housing["income_cat"].where(housing["income_cat"]<5, 5.0, inplace=True)
housing["income_cat"].value_counts() / len(housing)
from sklearn.model_selection import StratifiedShuffleSplit
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]
# Build a data pipeline
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, LabelBinarizer
num_attribs = list(housing)
num_attribs.remove('ocean_proximity')
cat_attribs = ['ocean_proximity']
class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.attribute_names].values
rooms_ix, bedrooms_ix, population_ix, household_ix = 3, 4, 5, 6
    
class CombineAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room = True):
        self.add_bedrooms_per_room = add_bedrooms_per_room
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        rooms_per_household = X[:, population_ix] / X[:, household_ix]
        population_per_household = X[:, population_ix] / X[:, household_ix]
        
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]
        
        else:
            return np.c_[X, rooms_per_household, population_per_household]
num_pipeline = Pipeline([
    ('selector', DataFrameSelector(num_attribs)),
    ('imputer', Imputer(strategy="median")),
    ('attribs_addr', CombineAttributesAdder()),
    ('std_scaler', StandardScaler()),
])
cat_pipeline = Pipeline([
    ('selector', DataFrameSelector(cat_attribs)),
    ('label_binarizer', LabelBinarizer())
])
full_pipeline = FeatureUnion(transformer_list=[
    ("num_pipeline", num_pipeline),
    ("cat_pipeline", cat_pipeline)
])
housing_prepared = full_pipeline.fit_transform(strat_train_set)
housing_prepared.shape
# Take care of missing values
from sklearn.preprocessing import Imputer
imputer = Imputer(strategy='median')
_strat_train_set_num = strat_train_set.drop("ocean_proximity", axis=1)
imputer.fit(_strat_train_set_num)
imputer.statistics_
X = imputer.transform(_strat_train_set_num)
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
housing_cat = strat_train_set['ocean_proximity']
housing_cat_encoded = encoder.fit_transform(housing_cat)
housing_cat_encoded
print(encoder.classes_)
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
housing_cat_1hot = encoder.fit_transform(housing_cat_encoded.reshape(-1,1))
housing_cat_1hot.toarray()
# Separate the predictors from labels
housing_pred = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()
housing.info()
housing.describe()
housing.hist(bins=70, figsize=(20, 15));
sns.jointplot(y="median_house_value", x="median_income", data=housing, size=10, alpha=0.2);
sns.FacetGrid(housing, hue="ocean_proximity", size=10)\
.map(plt.scatter, "median_house_value", "median_income", alpha=0.3)\
.add_legend();
housing.boxplot(column='median_house_value', by='ocean_proximity', rot=-45);
fig, ax = plt.subplots(figsize=(10,10))
sns.boxplot(y="median_house_value", x='ocean_proximity',  data=housing, orient='v', ax=ax);
sns.stripplot(x="ocean_proximity", y="median_house_value", data=housing, jitter=True, edgecolor="gray", ax=ax)
sns_plot = sns.pairplot(housing, hue="ocean_proximity", size=3)
sns_plot.savefig("pair_plot_.eps", format='eps', dpi=1000)
train_set.plot(kind='scatter', x='longitude', y='latitude', alpha=0.2);
sns.jointplot(x="longitude", y="latitude", data=train_set, size=10, alpha=0.2);
sns.FacetGrid(housing, hue="ocean_proximity", size=10).map(plt.scatter, "longitude", "latitude", alpha=0.2).add_legend();
train_set.corr()['median_house_value'].sort_values(ascending=False)
housing.corr()['median_house_value'].sort_values(ascending=False)
housing['median_income'].hist(bins=50)