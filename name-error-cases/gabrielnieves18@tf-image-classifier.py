# call %matplotlib only in a Jupiter notebook
# Common import
import hashlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import tarfile
from pandas.plotting import scatter_matrix
from six.moves import urllib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, cross_val_score
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import Imputer, LabelBinarizer, LabelEncoder
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = os.path.join("datasets", "housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"
def fetch_housing_data(housing_url=HOUSING_URL, 
                        housing_path=HOUSING_PATH):
    
        if not os.path.isdir(housing_path):
            os.makedirs(housing_path)
            
        tgz_path = os.path.join(housing_path, "housing.tgz")
        urllib.request.urlretrieve(housing_url, tgz_path)
        
        housing_tgz = tarfile.open(tgz_path)
        housing_tgz.extractall(path=housing_path)
        housing_tgz.close()
def load_housing_data(housing_path=HOUSING_PATH):
    
    csv_path = os.path.join(housing_path, "housing.csv")
    return( pd.read_csv(csv_path) )
def split_train_test(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return( data.iloc[train_indices], data.iloc[test_indices] )
def test_set_check(identifier, test_ratio, hash):
    hashed_id = hash(np.int64(identifier))
    return( hashed_id.digest()[-1] < (256 * test_ratio) )
def split_train_test_by_id(data, 
                           test_ratio, 
                           id_column, 
                           hash=hashlib.md5):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, 
                                                       test_ratio, 
                                                       hash))
    return( data.loc[~in_test_set], data.loc[in_test_set] )
def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())
# Although Scikit-Learn provides many useful transformers, 
# you will need to write your own for tasks such as custom 
# cleanup operations or combining specific attributes. 
#
# You will want your transformer to work seamlessly with 
# Scikit-Learn functionalities (such as pipelines), and 
# since Scikit-Learnrelies on duck typing (not inheritance), 
# all you need is to create a class and implement three 
# methods: fit() (returning self), transform(), and fit_transform(). 
#
# For more information reference page <To-Do: Add reference page number>
# 
from sklearn.base import BaseEstimator, TransformerMixin
rooms_ix, bedrooms_ix, population_ix, household_ix = 3, 4, 5, 6
class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room = True): # no *args or **kargs
        self.add_bedrooms_per_room = add_bedrooms_per_room
    def fit(self, X, y=None):
        return self  # nothing else to do
    def transform(self, X, y=None):
        rooms_per_household = X[:, rooms_ix] / X[:, household_ix]
        population_per_household = X[:, population_ix] / X[:, household_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household,
                         bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]
attr_adder = CombinedAttributesAdder(add_bedrooms_per_room=False)
housing_extra_attribs = attr_adder.transform(housing.values)
# Now it would be nice if we could feed a Pandas DataFrame containing 
# non-numerical columns directly into our pipeline, instead of having 
# to first manually extract the numerical columns into a NumPy array. 
#
# There is nothing in Scikit-Learn to handle Pandas DataFrames 
# but we can write a custom transformer for this task:
from sklearn.base import BaseEstimator, TransformerMixin
class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values
# 
# Disclaimer this is NOT the actual code from the book or
# the CategoricalEncoder definition.
#
# I created this class to prove a concept and play with ideas.
# For the real code see the github account for the book.
from sklearn.base import BaseEstimator, TransformerMixin
encoder = LabelBinarizer()
class MyCategoricalEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return encoder.fit(X)
    def transform(self, X, y=None):
        return encoder.transform(X.reshape(-1,1))
    def fit_transform(self, X, y=None):
        return encoder.fit_transform(X.reshape(-1,1))
# Definition of the CategoricalEncoder class, copied from PR #9151.
# Just run this cell, or copy it to your code, do not try to understand it (yet).
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import check_array
from sklearn.preprocessing import LabelEncoder
from scipy import sparse
class CategoricalEncoder(BaseEstimator, TransformerMixin):
    """Encode categorical features as a numeric array.
    The input to this transformer should be a matrix of integers or strings,
    denoting the values taken on by categorical (discrete) features.
    The features can be encoded using a one-hot aka one-of-K scheme
    (``encoding='onehot'``, the default) or converted to ordinal integers
    (``encoding='ordinal'``).
    This encoding is needed for feeding categorical data to many scikit-learn
    estimators, notably linear models and SVMs with the standard kernels.
    Read more in the :ref:`User Guide <preprocessing_categorical_features>`.
    Parameters
    ----------
    encoding : str, 'onehot', 'onehot-dense' or 'ordinal'
        The type of encoding to use (default is 'onehot'):
        - 'onehot': encode the features using a one-hot aka one-of-K scheme
          (or also called 'dummy' encoding). This creates a binary column for
          each category and returns a sparse matrix.
        - 'onehot-dense': the same as 'onehot' but returns a dense array
          instead of a sparse matrix.
        - 'ordinal': encode the features as ordinal integers. This results in
          a single column of integers (0 to n_categories - 1) per feature.
    categories : 'auto' or a list of lists/arrays of values.
        Categories (unique values) per feature:
        - 'auto' : Determine categories automatically from the training data.
        - list : ``categories[i]`` holds the categories expected in the ith
          column. The passed categories are sorted before encoding the data
          (used categories can be found in the ``categories_`` attribute).
    dtype : number type, default np.float64
        Desired dtype of output.
    handle_unknown : 'error' (default) or 'ignore'
        Whether to raise an error or ignore if a unknown categorical feature is
        present during transform (default is to raise). When this is parameter
        is set to 'ignore' and an unknown category is encountered during
        transform, the resulting one-hot encoded columns for this feature
        will be all zeros.
        Ignoring unknown categories is not supported for
        ``encoding='ordinal'``.
    Attributes
    ----------
    categories_ : list of arrays
        The categories of each feature determined during fitting. When
        categories were specified manually, this holds the sorted categories
        (in order corresponding with output of `transform`).
    Examples
    --------
    Given a dataset with three features and two samples, we let the encoder
    find the maximum value per feature and transform the data to a binary
    one-hot encoding.
    >>> from sklearn.preprocessing import CategoricalEncoder
    >>> enc = CategoricalEncoder(handle_unknown='ignore')
    >>> enc.fit([[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]])
    ... # doctest: +ELLIPSIS
    CategoricalEncoder(categories='auto', dtype=<... 'numpy.float64'>,
              encoding='onehot', handle_unknown='ignore')
    >>> enc.transform([[0, 1, 1], [1, 0, 4]]).toarray()
    array([[ 1.,  0.,  0.,  1.,  0.,  0.,  1.,  0.,  0.],
           [ 0.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.]])
    See also
    --------
    sklearn.preprocessing.OneHotEncoder : performs a one-hot encoding of
      integer ordinal features. The ``OneHotEncoder assumes`` that input
      features take on values in the range ``[0, max(feature)]`` instead of
      using the unique values.
    sklearn.feature_extraction.DictVectorizer : performs a one-hot encoding of
      dictionary items (also handles string-valued features).
    sklearn.feature_extraction.FeatureHasher : performs an approximate one-hot
      encoding of dictionary items or strings.
    """
    def __init__(self, encoding='onehot', categories='auto', dtype=np.float64,
                 handle_unknown='error'):
        self.encoding = encoding
        self.categories = categories
        self.dtype = dtype
        self.handle_unknown = handle_unknown
    def fit(self, X, y=None):
        """Fit the CategoricalEncoder to X.
        Parameters
        ----------
        X : array-like, shape [n_samples, n_feature]
            The data to determine the categories of each feature.
        Returns
        -------
        self
        """
        if self.encoding not in ['onehot', 'onehot-dense', 'ordinal']:
            template = ("encoding should be either 'onehot', 'onehot-dense' "
                        "or 'ordinal', got %s")
            raise ValueError(template % self.handle_unknown)
        if self.handle_unknown not in ['error', 'ignore']:
            template = ("handle_unknown should be either 'error' or "
                        "'ignore', got %s")
            raise ValueError(template % self.handle_unknown)
        if self.encoding == 'ordinal' and self.handle_unknown == 'ignore':
            raise ValueError("handle_unknown='ignore' is not supported for"
                             " encoding='ordinal'")
        X = check_array(X, dtype=np.object, accept_sparse='csc', copy=True)
        n_samples, n_features = X.shape
        self._label_encoders_ = [LabelEncoder() for _ in range(n_features)]
        for i in range(n_features):
            le = self._label_encoders_[i]
            Xi = X[:, i]
            if self.categories == 'auto':
                le.fit(Xi)
            else:
                valid_mask = np.in1d(Xi, self.categories[i])
                if not np.all(valid_mask):
                    if self.handle_unknown == 'error':
                        diff = np.unique(Xi[~valid_mask])
                        msg = ("Found unknown categories {0} in column {1}"
                               " during fit".format(diff, i))
                        raise ValueError(msg)
                le.classes_ = np.array(np.sort(self.categories[i]))
        self.categories_ = [le.classes_ for le in self._label_encoders_]
        return self
    def transform(self, X):
        """Transform X using one-hot encoding.
        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data to encode.
        Returns
        -------
        X_out : sparse matrix or a 2-d array
            Transformed input.
        """
        X = check_array(X, accept_sparse='csc', dtype=np.object, copy=True)
        n_samples, n_features = X.shape
        X_int = np.zeros_like(X, dtype=np.int)
        X_mask = np.ones_like(X, dtype=np.bool)
        for i in range(n_features):
            valid_mask = np.in1d(X[:, i], self.categories_[i])
            if not np.all(valid_mask):
                if self.handle_unknown == 'error':
                    diff = np.unique(X[~valid_mask, i])
                    msg = ("Found unknown categories {0} in column {1}"
                           " during transform".format(diff, i))
                    raise ValueError(msg)
                else:
                    # Set the problematic rows to an acceptable value and
                    # continue `The rows are marked `X_mask` and will be
                    # removed later.
                    X_mask[:, i] = valid_mask
                    X[:, i][~valid_mask] = self.categories_[i][0]
            X_int[:, i] = self._label_encoders_[i].transform(X[:, i])
        if self.encoding == 'ordinal':
            return X_int.astype(self.dtype, copy=False)
        mask = X_mask.ravel()
        n_values = [cats.shape[0] for cats in self.categories_]
        n_values = np.array([0] + n_values)
        indices = np.cumsum(n_values)
        column_indices = (X_int + indices[:-1]).ravel()[mask]
        row_indices = np.repeat(np.arange(n_samples, dtype=np.int32),
                                n_features)[mask]
        data = np.ones(n_samples * n_features)[mask]
        out = sparse.csc_matrix((data, (row_indices, column_indices)),
                                shape=(n_samples, indices[-1]),
                                dtype=self.dtype).tocsr()
        if self.encoding == 'onehot-dense':
            return out.toarray()
        else:
            return out
fetch_housing_data()
housing_data = load_housing_data()
housing_data.head()
housing_data.info()
housing_data['ocean_proximity'].value_counts()
housing_data.describe()
housing_data.hist(bins=50, figsize=(20, 15))
plt.show()
housing_data["income_cat"] = np.ceil(housing_data["median_income"] / 1.5)
# Add a values of 5.0 to the fields that return False to the
# condition. Otherwise, leave the current value in place
# get it; "inplace=True"; Soooo, leave the current value in place.
housing_data["income_cat"].where(housing_data["income_cat"] < 5, 
                                  5.0, 
                                  inplace=True)
housing_data.head()
# create your training and testing set
# Alternative 1
# housing_with_id = housing_data.reset_index()
# train_set, test_set = split_train_test_by_id(housing_with_id, 
#                                              0.20, 
#                                              "index")
# The scikit-learn way
'''
There is no particular reason for using 42 as our random_state.
This number has no special property, other than to be "The Answer
to the Ultimate Question of Life, The Universe, and Everything"
'''
train_set, test_set = train_test_split(housing_data, 
                                       test_size=0.2, 
                                       random_state=42)
print( "{} train + {} test".format(len(train_set), 
                                   len(test_set)) )
housing_data["median_income"].hist(bins=50, figsize=(15, 10))
plt.show()
housing_data["income_cat"].hist(bins=50, figsize=(10, 5))
plt.show()
overall = housing_data["income_cat"].value_counts(sort=False) / len(housing_data)
random_train = train_set["income_cat"].value_counts(sort=False) / len(train_set)
random_test = test_set["income_cat"].value_counts(sort=False) / len(test_set)
split = StratifiedShuffleSplit(n_splits=1,
                               test_size=0.2,
                               random_state=42)
for train_index, test_index in split.split(housing_data, 
                                       housing_data["income_cat"]):
    strat_train_set = housing_data.loc[train_index]
    strat_test_set = housing_data.loc[test_index]
    
strat_train = (strat_train_set["income_cat"].value_counts(sort=False) / len(train_set) )
strat_test = (strat_test_set["income_cat"].value_counts(sort=False) / len(test_set) )
# Lets test the homogeneity of out train and test sets
# in relation to the overall data set
hg_test = pd.DataFrame()
hg_test['Overall'] = overall
hg_test['Random Train'] = random_train
hg_test['Strat Train'] = strat_train
hg_test['Random Test'] = random_test
hg_test['Strat Test'] = strat_test
hg_test['Rand. Train %error'] = ((overall - random_train) / overall * 100).values
hg_test['Strat Train %error'] = ((overall - strat_train) / overall * 100).values
hg_test['Rand. Test %error'] = (( overall - random_test) / overall * 100).values
hg_test['Strat Test %error'] = ((overall - strat_test) / overall * 100).values
# Here we can see that the stratified sample is a better
# data set do to how much more homogeneous it is.
hg_test.iloc[::-1]
# Now we should remove the "income_cat" field so the data is back
# to its original state:
for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)
strat_test_set.head()
# Copy the training set to avoid loosing it
housing = strat_train_set.copy()
# Visualizing Geographical Data
housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4,
            s=housing["population"]/100, label="population", figsize=(10,7),
            c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=True)
# plt.legend()
plt.show()
# Another way to look for correlations between attributes 
# is to use Pandas scatter_matrix function.
attributes = ["median_house_value", "median_income", "total_rooms",
              "housing_median_age"]
scatter_matrix(housing[attributes], figsize=(12, 8))
plt.show()
# Now lets look for correlations
'''
See how the median income has 68% correlation with the 
mediam house value. This means that that people with 
higher income tend to have more expensive houses.
Who would have thought, right! -_-
Also, take a look at the latitud. It has a marginal negative 
correlation with the median house value. This means that
People that live in lower latitudes (farther from north) tend
to have higher median_house_income.
We can corroborate all this information on the scatter graph above.
'''
corr_mattrix = housing.corr()
corr_mattrix["median_house_value"].sort_values(ascending=False)
# median_house_value and median_income look promissing
# Lets take a closer look
housing.plot(kind="scatter", x="median_income", 
             y="median_house_value", alpha=0.4)
plt.show()
# Copy the training set to avoid loosing it
# Create the labels set aka. the "Y" vector
housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()
# Most Machine Learning algorithms cannot work with missing features, 
# let's use sklearn to populte these empty vaues with the respective 
# median value of each feature
imputer = Imputer(strategy="median")
# Imputer only works with numeric data, so lets create a copy of 
# our training set without the ocean_proximity
housing_num = housing.drop(labels="ocean_proximity", axis=1)
X = imputer.fit_transform(housing_num)
housing_tr = pd.DataFrame(X, columns=housing_num.columns)
imputer.statistics_
# Lets make sure that we have transform our data properly
# The pandas DataFrame.describe() method should be good for this.
# describe() will not count those values that are missing
housing_tr.describe()
# Eureka! We can see that all the features have a count of 16,512.
# That is the same as the lenght of the training set.
# All jokes aside. Now that we removed all missing values from our
# training set feat. we can move to fixing those pesky text fields.
# Earlier we left out the categorical atribute ocean_proximity because
# it is a text atribute so we cannot compute its median. 
# In a nutshell, most machine learning algorithms work with numbers
# So we need to convert these text values into integer that we can use 
# to map back and forward.
 
# We can use the Scikit-Learn utility LabelEncoder for this task
encoder = LabelEncoder()
housing_cat = housing["ocean_proximity"]
housing_cat_encoded = encoder.fit_transform(housing_cat)
housing_cat_encoded
# Awesome, now we have a numerical representaton of those text labels.
# The thing is, these numerical representations are not the best way 
# to deal with this kind of issue. Why you may ask?
# 
# Because Machine Learning Algorithms will assume that two near by
# values are more similar than two distant values. 
#
# A Common aproach to solving this issue it to represent the categories
# in a binary fashion, where we use 1 if it is "<1H OCEAN" and 0 otherwise.
# Because we have 5 catergories, we will need an array to represent each one.
# Ex:
#    "<1H OCEAN" = [1, 0, 0, 0, 0]
#    "INLAND" = [0, 1, 0, 0, 0]
#    "ISALAN" = [0, 0, 0, 1, 0]
#    etc...
#
# This is called "one-hot encoding", because only 1 atribute will be 
# equal to 1 (hot), while all others will be cero (cold).
# 
print(encoder.classes_)
encoder = OneHotEncoder()
housing_cat_1hot = encoder.fit_transform(housing_cat_encoded.reshape(-1,1))
housing_cat_1hot
# Im a bit sleepy right now, I have nothing witty to say
# See page 64 of the book for more info.
housing_cat_1hot.toarray()
num_attribs = list(housing_num)
cat_attribs = ["ocean_proximity"]
num_pipeline = Pipeline([
        ('selector', DataFrameSelector(num_attribs)),
        ('imputer', Imputer(strategy="median")),
        ('attribs_adder', CombinedAttributesAdder()),
        ('std_scaler', StandardScaler()) ])
# CategoricalEncoder is still not available in this version
# So I will re-use LabelBinarizer
#
# cat_pipeline = Pipeline([
#        ('selector', DataFrameSelector(cat_attribs)),
#        ('cat_encoder', CategoricalEncoder(encoding="onehot-dense")) ])
cat_pipeline = Pipeline([
       ('selector', DataFrameSelector(cat_attribs)),
       ('cat_encoder', MyCategoricalEncoder()) ])
full_pipeline = FeatureUnion(transformer_list=[
        ("num_pipeline", num_pipeline),
        ("cat_pipeline", cat_pipeline) ])
# Return a numpy array
housing_prepared = full_pipeline.fit_transform(housing)
housing_prepared
housing_prepared.shape
# Lest Train a Linear Regresion Model 
lin_reg = LinearRegression()
lin_reg.fit(housing_prepared, housing_labels)
some_data = housing.iloc[:5]
some_labels = housing_labels.iloc[:5]
some_data_prepared = full_pipeline.transform(some_data)
housing_predictions = lin_reg.predict(housing_prepared)
lin_mse = mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)
print("Predictions: {}".format(lin_reg.predict(some_data_prepared)))
print("Labels: {}".format(list(some_labels)))
print("Root Mean Squared Error (RMSE): {}".format(lin_rmse))
# We have an error margin of 68,628; Not too good.
# Let's try a NonLinearModel Model; Let's try DecisionTreeRegresor
tree_reg = DecisionTreeRegressor()
tree_reg.fit(housing_prepared, housing_labels)
housing_predictions = tree_reg.predict(housing_prepared)
tree_mse = mean_squared_error(housing_labels, housing_predictions)
tree_rmse = np.sqrt(tree_mse)
print("Predictions: {}".format(lin_reg.predict(some_data_prepared)))
print("Labels: {}".format(list(some_labels)))
print("Root Mean Squared Error (RMSE): {}".format(tree_rmse))
      
# OMG we have 0% error! We have created a perfect model.
# AKA. we have overfitted our data! #ZadBoyz
scores = cross_val_score(tree_reg, housing_prepared, housing_labels,
                         scoring="neg_mean_squared_error", cv=10)
tree_rmse_scores = np.sqrt(-scores)
display_scores(tree_rmse_scores)
lin_scores = cross_val_score(lin_reg, housing_prepared, housing_labels,
                             scoring="neg_mean_squared_error", cv=10)
lin_rmse_scores = np.sqrt(-lin_scores)
display_scores(lin_rmse_scores)
forest_reg = RandomForestRegressor()
forest_scores = cross_val_score(forest_reg, housing_prepared, housing_labels,
                                scoring="neg_mean_squared_error", cv=10)
forest_rmse_scores = np.sqrt(-forest_scores)
display_scores(forest_rmse_scores)
# To-Do