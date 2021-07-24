#!/usr/bin/env python
# coding: utf-8
# In[43]:
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
# In[37]:
transactions = pd.read_csv('transactions.csv')
customers_gender = pd.read_csv('customers_gender_train.csv')
# In[45]:
X = transactions.groupby('customer_id')                     .apply(lambda x: x[['mcc_code']].unstack().value_counts())                     .unstack()                     .fillna(0)
# In[47]:
customers_gender = customers_gender.set_index('customer_id')
# In[56]:
clf = GradientBoostingClassifier(random_state=13)
clf.fit(X_train, Y_train.values[:, 0]);
# In[54]:
X_test = X.drop(customers_gender.index)
result = pd.DataFrame(X_test.index, columns=['customer_id'])
result['gender'] = clf.predict_proba(X_test)[:, 1]