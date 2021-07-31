#!/usr/bin/env python
# coding: utf-8
# In[251]:
import numpy as np
import pandas as pd
# In[252]:
rawData = np.loadtxt(fname='disagreement-mturk-raw-ids-rankings-only.csv', delimiter=',', skiprows=1, 
                     dtype=np.dtype([('version', 'i4'), ('responseId', 'S25'), 
                                     ('rDA_1', 'f4'), ('rDA_2', 'f4'), ('rDA_3', 'f4'), ('rDA_4', 'f4'), ('rDA_5', 'f4'), 
                                     ('sDA_1', 'f4'), ('sDA_2', 'f4'), ('sDA_3', 'f4'), ('sDA_4', 'f4'), ('sDA_5', 'f4'), 
                                     ('rDB_1', 'f4'), ('rDB_2', 'f4'), ('rDB_3', 'f4'), ('rDB_4', 'f4'), ('rDB_5', 'f4'), 
                                     ('sDB_1', 'f4'), ('sDB_2', 'f4'), ('sDB_3', 'f4'), ('sDB_4', 'f4'), ('sDB_5', 'f4'), 
                                     ('rDC_1', 'f4'), ('rDC_2', 'f4'), ('rDC_3', 'f4'), ('rDC_4', 'f4'), ('rDC_5', 'f4'), 
                                     ('sDC_1', 'f4'), ('sDC_2', 'f4'), ('sDC_3', 'f4'), ('sDC_4', 'f4'), ('sDC_5', 'f4'), 
                                     ('rDD_1', 'f4'), ('rDD_2', 'f4'), ('rDD_3', 'f4'), ('rDD_4', 'f4'), ('rDD_5', 'f4'), 
                                     ('sDD_1', 'f4'), ('sDD_2', 'f4'), ('sDD_3', 'f4'), ('sDD_4', 'f4'), ('sDD_5', 'f4'), 
                                     ('mTurkCode', 'S25')]))
# initialize n-ary tree ranking results with headers
nTresults = [['datasetId', 
              'table_convertedR', 'table_confidence',
             'vis_convertedR', 'vis_confidence',
              'overall_convertedR', 'overall_confidence']]
# initialize summary results with headers
summaryResults = [['datasetId', 
              'table_convertedR', 'table_confidence',
             'vis_convertedR', 'vis_confidence',
              'overall_convertedR', 'overall_confidence']]
# full data frame
df = pd.DataFrame(rawData)
# Utils for statistics and all datasets, defining 'ground truth' columns in dataframes
overallDropCols = [50,51]
groupDropCols = [25, 26]
NtId = 50
# Ground Truth Ranking Datasets
datasetA_nTreeRanks = df.ix[df['version']==3].filter(['rDA_1', 'rDA_2', 'rDA_3', 'rDA_4', 'rDA_5']).T
datasetA_absRanks = df.ix[df['version']==4].filter(['rDA_1', 'rDA_2', 'rDA_3', 'rDA_4', 'rDA_5']).T
# In[253]:
# Dataset A
# Dataset A -- Table: Group 1 | Visualization: Group 2
datasetA_overall_ranks = df.filter(['rDA_1', 'rDA_2', 'rDA_3', 'rDA_4', 'rDA_5']).T
datasetA_group1_ranks = df.ix[(df['version']==1) | (df['version']==3) | (df['version']==4)].filter(['rDA_1', 'rDA_2', 'rDA_3', 'rDA_4', 'rDA_5']).T
datasetA_group2_ranks = df.ix[(df['version']==2) | (df['version']==3) | (df['version']==4)].filter(['rDA_1', 'rDA_2', 'rDA_3', 'rDA_4', 'rDA_5']).T
datasetA_overall_sliders = df.filter(['sDA_1', 'sDA_2', 'sDA_3', 'sDA_4', 'sDA_5']).T
datasetA_group1_sliders = df.ix[(df['version']==1) | (df['version']==3) | (df['version']==4)].filter(['sDA_1', 'sDA_2', 'sDA_3', 'sDA_4', 'sDA_5']).T
datasetA_group2_sliders = df.ix[(df['version']==2) | (df['version']==3) | (df['version']==4)].filter(['sDA_1', 'sDA_2', 'sDA_3', 'sDA_4', 'sDA_5']).T
# In[254]:
# Dataset B
# Dataset B -- Table: Group 1 | Visualization: Group 2
datasetB_overall_ranks = df.filter(['rDB_1', 'rDB_2', 'rDB_3', 'rDB_4', 'rDB_5']).T
datasetB_group1_ranks = df.ix[(df['version']==1) | (df['version']==3) | (df['version']==4)].filter(['rDB_1', 'rDB_2', 'rDB_3', 'rDB_4', 'rDB_5']).T
datasetB_group2_ranks = df.ix[(df['version']==2) | (df['version']==3) | (df['version']==4)].filter(['rDB_1', 'rDB_2', 'rDB_3', 'rDB_4', 'rDB_5']).T
datasetB_overall_sliders = df.filter(['sDB_1', 'sDB_2', 'sDB_3', 'sDB_4', 'sDB_5']).T
datasetB_group1_sliders = df.ix[(df['version']==1) | (df['version']==3) | (df['version']==4)].filter(['sDB_1', 'sDB_2', 'sDB_3', 'sDB_4', 'sDB_5']).T
datasetB_group2_sliders = df.ix[(df['version']==2) | (df['version']==3) | (df['version']==4)].filter(['sDB_1', 'sDB_2', 'sDB_3', 'sDB_4', 'sDB_5']).T
# In[255]:
# Dataset C
# Dataset C -- Table: Group 2 | Visualization: Group 1
datasetC_overall_ranks = df.filter(['rDC_1', 'rDC_2', 'rDC_3', 'rDC_4', 'rDC_5']).T
datasetC_group1_ranks = df.ix[(df['version']==1) | (df['version']==3) | (df['version']==4)].filter(['rDC_1', 'rDC_2', 'rDC_3', 'rDC_4', 'rDC_5']).T
datasetC_group2_ranks = df.ix[(df['version']==2) | (df['version']==3) | (df['version']==4)].filter(['rDC_1', 'rDC_2', 'rDC_3', 'rDC_4', 'rDC_5']).T
datasetC_overall_sliders = df.filter(['sDC_1', 'sDC_2', 'sDC_3', 'sDC_4', 'sDC_5']).T
datasetC_group1_sliders = df.ix[(df['version']==1) | (df['version']==3) | (df['version']==4)].filter(['sDC_1', 'sDC_2', 'sDC_3', 'sDC_4', 'sDC_5']).T
datasetC_group2_sliders = df.ix[(df['version']==2) | (df['version']==3) | (df['version']==4)].filter(['sDC_1', 'sDC_2', 'sDC_3', 'sDC_4', 'sDC_5']).T
# In[256]:
# Dataset D
# Dataset D -- Table: Group 2 | Visualization: Group 1
datasetD_overall_ranks = df.filter(['rDD_1', 'rDD_2', 'rDD_3', 'rDD_4', 'rDD_5']).T
datasetD_group1_ranks = df.ix[(df['version']==1) | (df['version']==3) | (df['version']==4)].filter(['rDD_1', 'rDD_2', 'rDD_3', 'rDD_4', 'rDD_5']).T
datasetD_group2_ranks = df.ix[(df['version']==2) | (df['version']==3) | (df['version']==4)].filter(['rDD_1', 'rDD_2', 'rDD_3', 'rDD_4', 'rDD_5']).T
datasetD_overall_sliders = df.filter(['sDD_1', 'sDD_2', 'sDD_3', 'sDD_4', 'sDD_5']).T
datasetD_group1_sliders = df.ix[(df['version']==1) | (df['version']==3) | (df['version']==4)].filter(['sDD_1', 'sDD_2', 'sDD_3', 'sDD_4', 'sDD_5']).T
datasetD_group2_sliders = df.ix[(df['version']==2) | (df['version']==3) | (df['version']==4)].filter(['sDD_1', 'sDD_2', 'sDD_3', 'sDD_4', 'sDD_5']).T
# In[257]:
# Ranks Summary Datasets
# Rank-Table Dataset
dataset_ranksTables = pd.concat([datasetA_group1_ranks, datasetB_group1_ranks, datasetC_group2_ranks, 
                                datasetD_group2_ranks])
# Rank-Vis Dataset
dataset_ranksVis = pd.concat([datasetA_group2_ranks, datasetB_group2_ranks, datasetC_group1_ranks, 
                                datasetD_group1_ranks])
# Ranks-Combined Dataset
dataset_ranksOverall = pd.concat([datasetA_overall_ranks, datasetB_overall_ranks, datasetC_overall_ranks, 
                                  datasetD_overall_ranks])
# In[258]:
# Sliders Summary Datasets
# Slider-Table Dataset
dataset_slidersTables = pd.concat([datasetA_group1_sliders, datasetB_group1_sliders, datasetC_group2_sliders, 
                                datasetD_group2_sliders])
# Slider-Vis Dataset
dataset_slidersVis = pd.concat([datasetA_group2_sliders, datasetB_group2_sliders, datasetC_group1_sliders, 
                                datasetD_group1_sliders])
# Sliders-Combined Dataset
dataset_slidersOverall = pd.concat([datasetA_overall_sliders, datasetB_overall_sliders, datasetC_overall_sliders, 
                                  datasetD_overall_sliders])
# In[259]:
def fisherTransform(corr):
    '''
    Given 1-row matrix of correlation coefficients, computes Fisher Transform matrix of same dimensions
    Equivalent to: F = adjustedCorr.applymap(lambda r: 0.5*np.log((1+r)/(1-r)))
    '''
    
    # Treat correlation of 1 as 0.9999 to prevent undefined values
    adjustedCorr = corr.applymap(lambda x: 0.999 if (x == 1.0) else x)
    adjustedCorr = adjustedCorr.applymap(lambda x: -0.999 if (x == -1.0) else x)
    
    # Fisher transform all the correlation coefficients (equivalent to hyperbolic tangent)
    F = np.arctanh(adjustedCorr)
    
    return F
# In[260]:
def avgFisherTransform(F):
    '''Given 1-row Matrix of Fisher Transform Values, returns Average Fisher Transform'''
    return F.mean(axis=1)
# In[261]:
def fisherStdErr(n):
    '''Given sample size n, returns standard error for Fisher Transform'''
    return (1/np.sqrt(n-3))
# In[262]:
def confidenceInterval(refP, critZ, stdErr):
    '''
    Given a reference point (generally mean of dataset) and standard error value, returns confidence interval
    low = refP - (critZ * stdErr)
    high = refP + (critZ * stdErr)
    '''
    low = refP - (critZ * stdErr)
    high = refP + (critZ * stdErr)
    
    return low, high
# In[263]:
def convertZtoR(zVal):
    '''
    Given Fisher Transform z val, computes r Correlation Coefficient
    Equivalent to return (np.exp(2*zVal)-1) / (np.exp(2*zVal)+1)
    '''
    return np.tanh(zVal)
# In[264]:
def computeStats(df, dropCols, gtId, statsMethod):
    '''Helper function for buildStats. Given dataframe, indices for columns to drop, and 
    index for the ground truth ranking id, and stats method, it returns tuple of coefficients'''
    # all correlations
    corr = df.corr(method=statsMethod, min_periods=5)
    # correlations with n-ary tree ranking
    #TODO: these indices might need to be updated if we add absolute ranking
    nTOverall = corr[-2:-1].drop(corr.columns[dropCols],axis=1)
    # average n-ary tree correlation
    avgNtOverall = nTOverall.mean(axis=1)
    avgR = avgNtOverall[gtId]
    
    # average F-transform of n-ary tree metric
    fTransform = fisherTransform(nTOverall)
    avgFvec = avgFisherTransform(fTransform)
    avgF = avgFvec[gtId]
    
    # sample size (n is number of columns, which is sample size)
    m, n = corr.shape
    
    # stdErr on fisher transform
    fStdErr = fisherStdErr(n)
    
    # use Z criterion of 1.96 for 95% confidence interval
    critZ = 1.96
    
    # confidence interval
    fLow, fHigh = confidenceInterval(avgF, critZ, fStdErr)
    rLow = convertZtoR(fLow)
    rHigh = convertZtoR(fHigh)
    
    # converted (transformed) average correlation coeff
    convAvgRvec = convertZtoR(avgFvec)
    convR = convAvgRvec[gtId]
    
    return convR, (rLow, rHigh)
# In[265]:
def buildStats(dataId, tableGroup, visGroup, overall, statsMethod):
    '''Given a dataset label, overall data set and dataset for each group, returns list of results'''
    
    #initialize empty list of stats
    stats=[dataId]
    
    # table data
    tableGroupR, tableGroupConf = computeStats(tableGroup, groupDropCols, NtId, statsMethod)
    stats.append(tableGroupR)
    stats.append(tableGroupConf)
    
    # vis data
    visGroupR, visGroupConf = computeStats(visGroup, groupDropCols, NtId, statsMethod)
    stats.append(visGroupR)
    stats.append(visGroupConf)
        
    # overall data
    overallR, overallConf = computeStats(overall, overallDropCols, NtId, statsMethod)
    stats.append(overallR)
    stats.append(overallConf)
    
    
    return stats
    
# In[266]:
# Dataset A -- Table: Group 1 | Visualization: Group 2
aRanksPearson = buildStats('datasetA_ranks_pearson', datasetA_group1_ranks, datasetA_group2_ranks, 
                           datasetA_overall_ranks, 'pearson')
nTresults.append(aRanksPearson)
# Dataset B -- Table: Group 1 | Visualization: Group 2
bRanksPearson = buildStats('datasetB_ranks_pearson', datasetB_group1_ranks, datasetB_group2_ranks,
                           datasetB_overall_ranks, 'pearson')
nTresults.append(bRanksPearson)
# Dataset C -- Table: Group 2 | Visualization: Group 1
cRanksPearson = buildStats('datasetC_ranks_pearson', datasetC_group2_ranks, datasetC_group1_ranks,
                           datasetC_overall_ranks, 'pearson')
nTresults.append(cRanksPearson)
# Dataset D -- Table: Group 2 | Visualization: Group 1
dRanksPearson = buildStats('datasetD_ranks_pearson', datasetD_group2_ranks, datasetD_group1_ranks, 
                           datasetD_overall_ranks, 'pearson')
nTresults.append(dRanksPearson)
# Summary Stats
allRanksPearson = buildStats('ranks_dataset', dataset_ranksTables, dataset_ranksVis, 
                             dataset_ranksOverall, 'pearson')
summaryResults.append(allRanksPearson)
# In[267]:
# Dataset A -- Table: Group 1 | Visualization: Group 2
aSlidersSpearman = buildStats('datasetA_sliders_spearman', datasetA_group1_sliders, datasetA_group2_sliders, 
                           datasetA_overall_sliders, 'spearman')
nTresults.append(aSlidersSpearman)
# Dataset B -- Table: Group 1 | Visualization: Group 2
bSlidersSpearman = buildStats('datasetB_sliders_spearman', datasetB_group1_sliders, datasetB_group2_sliders,
                           datasetB_overall_sliders, 'spearman')
nTresults.append(bSlidersSpearman)
# Dataset C -- Table: Group 2 | Visualization: Group 1
cSlidersSpearman = buildStats('datasetC_sliders_spearman', datasetC_group2_sliders, datasetC_group1_sliders,
                           datasetC_overall_sliders, 'spearman')
nTresults.append(cSlidersSpearman)
# Dataset D -- Table: Group 2 | Visualization: Group 1
dSlidersSpearman = buildStats('datasetD_sliders_spearman', datasetD_group2_sliders, datasetD_group1_sliders, 
                           datasetD_overall_sliders, 'spearman')
nTresults.append(dSlidersSpearman)
# Summary Stats
allSlidersSpearman = buildStats('sliders_dataset', dataset_slidersTables, dataset_slidersVis, 
                             dataset_slidersOverall, 'spearman')
summaryResults.append(allSlidersSpearman)
# In[268]:
print(nTresults)
print (summaryResults)
# In[269]:
outputDf = pd.DataFrame(nTresults)
outputDf.to_csv('nTreeStats.csv', index=False, header=False)
summaryDF = pd.DataFrame(summaryResults)
summaryDF.to_csv('SummaryStats.csv', index=False, header=False)