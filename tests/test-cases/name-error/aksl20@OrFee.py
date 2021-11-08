#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint
sns.set()
get_ipython().run_line_magic('matplotlib', 'inline')
# In[3]:
from IPython.display import HTML
HTML('''<script>
code_show=true; 
function code_toggle() {
if (code_show){
$('div.input').hide();
} else {
$('div.input').show();
}
code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<a href="javascript:code_toggle()">Click here to hide/print cells code</a>.''')
# In[2]:
candidates = pd.read_csv('data/data_v1.0.csv').drop(['Unnamed: 0', 'index'], axis=1)
# In[3]:
candidates.head()
# In[36]:
print('Nombre de lignes: {}\n'
      'Nombre de colonnes: {}'.format(*candidates.shape))
# In[16]:
candidates.describe()
# In[4]:
candidates.select_dtypes(include=['object']).describe()
# In[3]:
for column in candidates.columns:
    most_common = candidates[column].value_counts().keys()[0]
    candidates[column] = candidates[column].fillna(most_common)
    print('{} : {} valeurs'.format(column, str(candidates[column].count())))
candidates.loc[candidates['exp'] < 0, ('exp')] = candidates['exp'].mean()
candidates.loc[candidates['age'] < 3, ('age')] = candidates['age'].mean()
# In[4]:
hired = candidates[candidates['embauche'] == 1]
rejected = candidates[candidates['embauche'] == 0]
# In[139]:
candidates['date'] = pd.to_datetime(candidates['date'], dayfirst=True)
groupeby_date = candidates.loc[:, ('date', 'embauche')].groupby('date').sum()
groupeby_date_mounth = groupeby_date.groupby(pd.Grouper(freq="M")).sum()
_ = groupeby_date_mounth.plot()
_ = plt.ylabel('Nombre d\'embauche')
# In[114]:
_ = sns.boxplot(x='cheveux', y='note', data=hired)
# In[122]:
_ = plt.hist([hired.salaire.sample(n=2000), rejected.salaire.sample(n=2000).values])
_ = plt.legend(['Embauché', 'Rejeté'])
_ = plt.ylabel('Count')
_ = plt.xlabel('Salaires')
# In[34]:
fig, axs = plt.subplots(ncols=2, figsize=(14, 6))
_ = sns.boxplot(x='diplome', y='salaire', hue='embauche', data=candidates, ax=axs[0])
_ = sns.boxplot(x='specialite', y='salaire', hue='embauche', data=candidates, ax=axs[1])
# In[35]:
fig, axs = plt.subplots(ncols=2, figsize=(14, 6))
_ = sns.boxplot(x='diplome', y='note', hue='embauche', data=candidates, ax=axs[0])
_ = sns.boxplot(x='specialite', y='note', hue='embauche', data=candidates, ax=axs[1])
# In[11]:
notes = candidates['note']
exp = candidates['exp']
# In[18]:
notes_jit = jitter(notes)
exp_jit = jitter(exp)
# In[22]:
_ = sns.jointplot(x=notes_jit, y=exp_jit, kind='reg')
# In[88]:
_ = sns.countplot(x='specialite', hue='sexe', data=candidates)
# In[79]:
from sklearn.preprocessing import LabelEncoder
lb_sexe = LabelEncoder()
lb_specialite = LabelEncoder()
df['sexe'] = lb_sexe.fit_transform(df['sexe'])
df['specialite'] = lb_specialite.fit_transform(df['specialite'])
# In[86]:
df.corr(method='pearson')
# In[238]:
_ = sns.boxplot(x='cheveux', y='salaire', data=candidates)
# In[138]:
from sklearn.preprocessing import LabelEncoder
df = candidates.copy()
lb_cheveux = LabelEncoder()
df['cheveux'] = lb_cheveux.fit_transform(df['cheveux'])
# In[119]:
df.loc[:, ('cheveux', 'salaire')].corr(method='pearson')
# In[37]:
def get_cdf(sample, x):
    count = 0.0
    for value in sample:
        if value <= x:
            count += 1
    prob = count / len(sample)
    return prob
# In[38]:
women = candidates[candidates['sexe'] == 'F']
men = candidates[candidates['sexe'] == 'M']
ages_men = men['age']
ages_women = women['age']
# In[40]:
ages_men_cdf = [get_cdf(ages_men, x) for x in ages_men.sort_values()]
ages_women_cdf = [get_cdf(ages_women, x) for x in ages_women.sort_values()]
pprint('Homme : {}'.format(ages_men_cdf[:10]))
pprint('Femme : {}'.format(ages_women_cdf[:10]))
# In[108]:
_= plt.plot(ages_men.sort_values(), ages_men_cdf, ages_women.sort_values(), ages_women_cdf)
_ = plt.ylabel('Cdf')
_ = plt.xlabel('Ages')
_ = plt.legend(['M', 'F'])
# In[5]:
# Create a copy of original candidates dataframe
data = candidates.copy()
# Select categorical columns
dummy_columns = ['sexe', 'specialite', 'cheveux', 'dispo', 'diplome']
for each in dummy_columns:
    dummies = pd.get_dummies(data[each], prefix=each, drop_first=False)
    data = pd.concat([data, dummies], axis=1)
# drop old and useless columns
columns_to_drop = ['date', 'cheveux', 'sexe', 'diplome', 'specialite', 'dispo', 'age']
data = data.drop(columns_to_drop, axis=1).copy()
data.head()
# In[6]:
from sklearn.model_selection import train_test_split
target_columns = ['embauche']
features, target = data.drop(target_columns, axis=1), data[target_columns]
train_features, test_features, train_target, test_target = train_test_split(
        features, target, test_size=0.30)
# In[7]:
from pprint import pprint
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 10, stop = 200, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
pprint(random_grid)
# In[9]:
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf_random = RandomizedSearchCV(estimator=rf, refit=True, param_distributions=random_grid, 
                               n_iter=100, cv=3, verbose=0, random_state=42, n_jobs=-1)
# In[80]:
# Compute our random search to get best parameters
rf_random.fit(train_features[:].values, train_target['embauche'].values)
# In[87]:
print('Meilleurs paramètres:')
rf_random.best_params_
# In[32]:
# Init our model with parameters found previously
rf = RandomForestClassifier(max_features='sqrt', n_estimators=136, 
                            max_depth=80, min_samples_split=2,
                            min_samples_leaf=4, bootstrap=False)
pprint('Paramètre de notre model : {}'.format(rf.get_params()))
# In[69]:
print('Fit... and Predict...')
prediction = rf.fit(train_features[:].values, train_target['embauche'].values).predict(test_features[:].values)
print('==> predict: ')
reality = test_target[:].values
result = pd.DataFrame({'prediction': prediction, 'reality': test_target['embauche']})
result['get_it'] = 'nop'
result.loc[result.prediction == result.reality, 'get_it'] = 'yes'
print(result[30:50])
print('  == get_it:')
print(result.get_it.value_counts())
# Print score for test and train features
print('Score on train dataset : {0:.3f}\n'
      'Score on test dataset : {1:.3f}\n'.format(rf.score(train_features, train_target),
                                            rf.score(test_features, test_target)))