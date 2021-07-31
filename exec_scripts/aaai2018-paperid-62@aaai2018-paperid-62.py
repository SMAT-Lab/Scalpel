#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn', hides SettingWithCopyWarning
file = 'data/evaluations.csv'
conversion_dict = {'research_type': lambda x: int(x == 'E')}
evaluation_data = pd.read_csv(file, sep=',', header=0, index_col=0, converters=conversion_dict)
print('Samples per conference\n{}'.format(evaluation_data.groupby('conference').size()), end='\n')
column_headers = evaluation_data.columns.values
print('\nColumn headers: {}'.format(column_headers))
# In[2]:
evaluation_data.drop(['title', 'authors', 'link', 'comments'], axis=1, inplace=True)
column_headers = evaluation_data.columns.values
evaluation_data.head(2)
# In[3]:
print('Samples per affiliation\n{}'.format(evaluation_data.groupby('affiliation').size()), end='\n\n')
print('Affiliation by conference\n{}'.format(evaluation_data.groupby(['conference', 'affiliation']).size()), end='\n\n')
print('Samples per research type\n{}'.format(evaluation_data.groupby('research_type').size()), end='\n\n')
print('Research type by conference\n{}'.format(evaluation_data.groupby(['conference', 'research_type']).size()), end='\n\n')
print('Samples per research outcome\n{}'.format(evaluation_data.groupby('result_outcome').size()), end='\n\n')
print('Research outcome by conference\n{}'.format(evaluation_data.groupby(['conference', 'result_outcome']).size()), end='\n\n')
print('Samples with contribution\n{}'.format(evaluation_data.groupby('contribution').size()), end='\n\n')
print('Contribution by conference\n{}'.format(evaluation_data.groupby(['conference', 'contribution']).size()), end='\n\n')
# In[4]:
experimental_data = evaluation_data[evaluation_data.research_type == 1]
early_years_index = (experimental_data.conference == 'AAAI 14') | (experimental_data.conference == 'IJCAI 13')
late_years_index = (experimental_data.conference == 'AAAI 16') | (experimental_data.conference == 'IJCAI 16')
# In[5]:
method = ['conference','problem_description','goal/objective','research_method',
        'research_question','pseudocode']
r3_columns = method
experimental_data.loc[:, 'R3'] = experimental_data[r3_columns].all(axis=1)
print('R3(e)\nTotal = {}'.format(experimental_data['R3'].sum()))
display(experimental_data[['R3', 'conference']].groupby('conference').sum())
experimental_data.loc[:, 'R3D'] = experimental_data[r3_columns].mean(axis=1)
print('\n\nR3D\nTotal: {:.4f}, variance = {:.4f}\nBy conference, followed by variance'
      .format(experimental_data['R3D'].mean(), experimental_data['R3D'].var()))
display(experimental_data[['R3D', 'conference']].groupby('conference').mean())
display(experimental_data[['R3D', 'conference']].groupby('conference').var())
print('\n\nYear\tR3D\tVariance\n2013/14\t{:.4f}\t{:.4f}'.format(
    experimental_data[early_years_index].R3D.mean(),
    experimental_data[early_years_index].R3D.var()))
print('2016\t{:.4f}\t{:.4f}'.format(
    experimental_data[late_years_index].R3D.mean(),
    experimental_data[late_years_index].R3D.var()))
# In[6]:
data = ['train', 'validation', 'test', 'results']
r2_columns = r3_columns + data
experimental_data.loc[:, 'Data'] = experimental_data[data].all(axis=1)
print('Data(e)\nTotal = {:}'.format(experimental_data['Data'].sum()))
display(experimental_data[['Data', 'conference']].groupby('conference').sum())
experimental_data.loc[:, 'DataD'] = experimental_data[data].mean(axis=1)
print('\n\nDataDegree(e)\nTotal = {:.4f}, variance = {:.4f}\nBy conference, followed by variance'
      .format(experimental_data['DataD'].mean(), experimental_data['DataD'].var()))
display(experimental_data[['DataD', 'conference']].groupby('conference').mean())
display(experimental_data[['DataD', 'conference']].groupby('conference').var())
print('\n\nYear\tDataD\tVariance\n2013/14\t{:.4f}\t{:.4f}'.format(
    experimental_data[early_years_index].DataD.mean(),
    experimental_data[early_years_index].DataD.var()))
print('2016\t{:.4f}\t{:.4f}'.format(
    experimental_data[late_years_index].DataD.mean(),
    experimental_data[late_years_index].DataD.var()))
experimental_data.loc[:, 'R2'] = experimental_data[r2_columns].all(axis=1)
print('\n\nR2(e)\nTotal = {}'.format(experimental_data['R2'].sum()))
display(experimental_data[['R2', 'conference']].groupby('conference').sum())
experimental_data.loc[:, 'R2D'] = experimental_data[r2_columns].mean(axis=1)
print('\n\nR2D(e)\nTotal = {:.4f}, variance = {:.4f}\nBy conference, followed by variance'
      .format(experimental_data['R2D'].mean(), experimental_data['R2D'].var()))
display(experimental_data[['R2D', 'conference']].groupby('conference').mean())
display(experimental_data[['R2D', 'conference']].groupby('conference').var())
print('\n\nYear\tR2D\tVariance\n2013/14\t{:.4f}\t{:.4f}'.format(
    experimental_data[early_years_index].R2D.mean(),
    experimental_data[early_years_index].R2D.var()))
print('2016\t{:.4f}\t{:.4f}'.format(
    experimental_data[late_years_index].R2D.mean(),
    experimental_data[late_years_index].R2D.var()))
# In[7]:
experiment = ['hypothesis', 'prediction',
        'open_source_code', 'open_experiment_code',
        'hardware_specification', 'software_dependencies',
        'experiment_setup', 'evaluation_criteria']
r1_columns = r2_columns + experiment
experimental_data.loc[:, 'Exp'] = experimental_data[experiment].all(axis=1)
print('Exp(e)\nTotal = {:.4f}'.format(experimental_data['Exp'].sum()))
display(experimental_data[['Exp', 'conference']].groupby('conference').sum())
experimental_data.loc[:, 'ExpD'] = experimental_data[experiment].mean(axis=1)
print('\n\nExpDegree(e)\nTotal = {:.4f}, variance = {:.4f}\nBy conference, followed by variance'
      .format(experimental_data['ExpD'].mean(), experimental_data['ExpD'].var()))
display(experimental_data[['ExpD', 'conference']].groupby('conference').mean())
display(experimental_data[['ExpD', 'conference']].groupby('conference').var())
print('\n\nYear\tExpD\tVariance\n2013/14\t{:.4f}\t{:.4f}'.format(
    experimental_data[early_years_index].ExpD.mean(),
    experimental_data[early_years_index].ExpD.var()))
print('2016\t{:.4f}\t{:.4f}'.format(
    experimental_data[late_years_index].ExpD.mean(),
    experimental_data[late_years_index].ExpD.var()))
experimental_data.loc[:, 'R1'] = experimental_data[r1_columns].all(axis=1)
print('\n\nR1(e)\nTotal = {:.4f}'.format(experimental_data['R1'].sum()))
display(experimental_data[['R1', 'conference']].groupby('conference').sum())
experimental_data.loc[:, 'R1D'] = experimental_data[r1_columns].mean(axis=1)
print('\n\nR1D(e)\nTotal = {:.4f}, variance = {:.4f}\nBy conference, followed by variance'
      .format(experimental_data['R1D'].mean(), experimental_data['R1D'].var()))
display(experimental_data[['R1D', 'conference']].groupby('conference').mean())
display(experimental_data[['R1D', 'conference']].groupby('conference').var())
print('\n\nYear\tR1D\tVariance\n2013/14\t{:.4f}\t{:.4f}'.format(
    experimental_data[early_years_index].R1D.mean(),
    experimental_data[early_years_index].R1D.var()))
print('2016\t{:.4f}\t{:.4f}'.format(
    experimental_data[late_years_index].R1D.mean(),
    experimental_data[late_years_index].R1D.var()))
# In[8]:
import IPython
import platform
print('Python version: {}'.format(platform.python_version()))
print('IPython version: {}'.format(IPython.__version__))
print('pandas version: {}'.format(pd.__version__))