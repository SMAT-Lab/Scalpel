#!/usr/bin/env python
# coding: utf-8
# In[1]:
import os
limit = 3
def ngrams(lines):
    global limit
    ngrams = []
    for i in range(1, limit+1):
        ndict = {}
        for line in lines:
            nline = ['<START>']*i + line + ['<END>']*i
            for x in range(len(nline)- i) :
                key = '_'.join(nline[x:x+i])
                if key in ndict.keys():
                    ndict[key] += 1
                else:
                    ndict[key] = 1
        ngrams += [ndict]
        print ("ngrams",ngrams)
    return ngrams
def cleanLines(lines):
    for i in range(len(lines)):
        lines[i] = lines[i][:-1].split()
        for x in range(len(lines[i])):
            lines[i][x] = lines[i][x].lower()
    return lines
def score(uinput, tngramsdict):
    global limit
    scores = []
    uinput = [uinput.lower().split()]
    cur_ngramsdict = ngrams(uinput)
    for key in tngramsdict:
        ngramsdict = tngramsdict[key]
        fscore = 0.0
        for i in range(len(cur_ngramsdict)):
            cur_dict = cur_ngramsdict[i]
            ansdict = ngramsdict[i]
            precision = 0
            for i in cur_dict.keys():
                if i in ansdict.keys():
                    precision+=1
            recall = 0
            for i in ansdict.keys():
                if i in cur_dict.keys():
                    recall+=1
            fscore += 1.0/float((len(ansdict.keys())/float(precision) + len(ansdict.keys())/float(recall)))
        scores+= [(key,fscore)]
    return scores
def init():
    ngramsdict = {}
    path = './intents/'
    for fil in os.listdir(path):
        if fil.endswith('.dat'):
            with open(path + fil) as f:
                lines = f.readlines()
                lines = cleanLines(lines)
                ngramsdict[''.join(fil.split('.')[:-1])] = ngrams(lines)
    return ngramsdict
def ngrammatch(uinput):
    ngramsdict = init()
    scores = score(uinput, ngramsdict)
    #print scores
    return scores
# In[3]:
ngrammatch("want a laptop")