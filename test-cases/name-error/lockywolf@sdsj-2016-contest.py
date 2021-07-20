import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
transactions = pd.read_csv('transactions.csv')
customers_gender = pd.read_csv('customers_gender_train.csv')
X = transactions.groupby('customer_id') \
                    .apply(lambda x: x[['mcc_code']].unstack().value_counts()) \
                    .unstack() \
                    .fillna(0)
customers_gender = customers_gender.set_index('customer_id')
Y_train = customers_gender.loc[X.index].gender
Y_train = Y_train.reset_index()
del Y_train['customer_id']
Y_train = Y_train.dropna(0)
X_train = X.reset_index()
X_train = X_train.loc[Y_train.index].set_index('customer_id')
clf = GradientBoostingClassifier(random_state=13)
clf.fit(X_train, Y_train.values[:, 0]);
X_test = X.drop(customers_gender.index)
result = pd.DataFrame(X_test.index, columns=['customer_id'])
result['gender'] = clf.predict_proba(X_test)[:, 1]
result.to_csv('baseline_a.csv', index=False)