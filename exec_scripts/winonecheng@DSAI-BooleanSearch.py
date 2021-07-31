#!/usr/bin/env python
# coding: utf-8
# In[1]:
import csv
import re
# In[2]:
eng_dict = dict()
ch2_dict = dict()
ch3_dict = dict()
# In[3]:
def tokenize(str):
    eng_match = re.findall(r'[a-zA-Z]{2,}', str)
    ch2_match = re.findall(r'(?=([\u4e00-\u9fff]{2}))', str)
    ch3_match = re.findall(r'(?=([\u4e00-\u9fff]{3}))', str)
    return [eng_match, ch2_match, ch3_match]
# In[4]:
def build_inverted_index(eng_match, ch2_match, ch3_match, index):
    for gram in ch2_match:
        if gram not in ch2_dict:
            ch2_dict[gram] = [index]
        else:
            ch2_dict[gram].append(index)
    for gram in ch3_match:
        if gram not in ch3_dict:
            ch3_dict[gram] = [index]
        else:
            ch3_dict[gram].append(index)
    for gram in eng_match:
        if gram not in eng_dict:
            eng_dict[gram] = [index]
        else:
            eng_dict[gram].append(index)
# In[8]:
get_ipython().run_cell_magic('time', '', "with open('source.csv', newline='') as f:\n    reader = csv.reader(f, delimiter=',')\n    index = 1\n    for row in reader:\n        matches = tokenize(row[1])\n        build_inverted_index(*matches, index)\n        index += 1")
# In[6]:
def bool_search(words, oper):
    index = list()
    for word in words:
        match = re.search('[a-zA-Z]', word)
        if match:
            index.append(eng_dict[word])
        elif len(word) == 2:
            index.append(ch2_dict[word])
        elif len(word) == 3:
            index.append(ch3_dict[word])
            
    if oper is 'and':
        return list(set(index[0]).intersection(*index[1:]))
    elif oper is 'or':
        return list(set(index[0]).union(*index[1:]))
    elif oper is 'not':
        return list(set(index[0]).difference(*index[1:]))
# In[7]:
get_ipython().run_cell_magic('time', '', "with open('query.txt', 'r') as f:\n    with open('output.txt', 'w') as fout:\n        for row in f.readlines():\n            row = row.strip()\n            if 'and' in row:\n                words = re.split(r' and ', row)\n                result = bool_search(words, 'and')\n\n            elif 'or' in row:\n                words = re.split(r' or ', row)\n                result = bool_search(words, 'or')\n\n            elif 'not' in row:\n                words = re.split(r' not ', row)\n                result = bool_search(words, 'not')\n\n            if len(result) != 0:\n                fout.write(','.join([str(index) for index in sorted(result)]) + '\\n')\n            else:\n                fout.write('0\\n')\n        \n        # Remove the last new line\n        fout.seek(fout.tell()-1)\n        fout.truncate()")