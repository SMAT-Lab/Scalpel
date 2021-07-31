#!/usr/bin/env python
# coding: utf-8
# In[53]:
# python --
len(list(open('data/hightemp.txt')))
# In[19]:
# unix --
get_ipython().system('wc -l  data/hightemp.txt')
# In[54]:
# python --
print(''.join([line.replace('\t', ' ') for line in  list(open('data/hightemp.txt'))]))
# In[21]:
# unix --
# !gsed -e "s/\t/ /g" data/hightemp.txt
# !cat data/hightemp.txt | tr '\t' ' '
get_ipython().system('expand  -t 1 data/hightemp.txt')
# In[55]:
# python -- 
with open('output/col1.txt', 'w') as col1,    open('output/col2.txt', 'w') as col2:
    for line in list(open('data/hightemp.txt')):
        col1.write(line.strip().split('\t')[0] + '\n')
        col2.write(line.strip().split('\t')[1] + '\n')
# In[23]:
# unix --
get_ipython().system('cut -f 1 data/hightemp.txt > output/col1_unix.txt')
get_ipython().system('cut -f 2 data/hightemp.txt > output/col2_unix.txt')
# In[24]:
# 差分チェック
get_ipython().system('diff output/col1.txt output/col1_unix.txt ')
get_ipython().system('diff output/col2.txt output/col2_unix.txt')
# In[57]:
# python --
with open('output/col1.txt') as col1,    open('output/col2.txt') as col2,    open('output/col1_col2_merge.txt', 'w') as merge:
    for c1, c2 in zip(list(col1),  list(col2)):
        merge.write('\t'.join([c1.strip(), c2.strip()]) + '\n')
# In[26]:
# unix --
get_ipython().system('paste output/col1.txt output/col2.txt > output/col1_col2_merge_unix.txt')
# In[27]:
# 差分チェック
get_ipython().system('diff output/col1_col2_merge.txt output/col1_col2_merge_unix.txt ')
# In[60]:
# python --
# 引数を受け取るとしたら
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('--num', '-n', help='number of lines', default=3)
# args = parser.parse_args()
# num = args.num
num = 3
print(''.join(list(open('data/hightemp.txt'))[:num]))
# In[29]:
# unix --
get_ipython().system('head -n 3 data/hightemp.txt')
# In[30]:
# python --
num = 3
print(''.join(list(open('data/hightemp.txt'))[-num:]))
# In[61]:
# unix --
get_ipython().system('tail -n 3 data/hightemp.txt')
# In[32]:
# python --
num = 3
all_lines = list(open('data/hightemp.txt'))
for number, lines in enumerate([all_lines[i: i + num] for i in range(0, len(all_lines), num)]):
    with open('output/hightemp_split_{}.txt'.format(number), 'w') as fp:
        fp.writelines(lines)
# In[36]:
# unix --
get_ipython().system('split -l 3 data/hightemp.txt output/hightemp_split_')
# In[39]:
# python --
{l.split('\t')[0] for l in list(open('data/hightemp.txt'))}
# In[38]:
# unix --
get_ipython().system(' cut -f 1 data/hightemp.txt | sort | uniq -c | cut -c 6-')
# In[46]:
# python --
print(''.join(sorted(list(open('data/hightemp.txt')), key = lambda x: x.split('\t')[2], reverse=True)))
# In[40]:
# unix --
get_ipython().system('sort -r -k 3 data/hightemp.txt')
# In[48]:
# unix --
get_ipython().system('cut -f 1 data/hightemp.txt | sort | uniq -c | sort -r ')
# In[51]:
# python --
from collections import Counter
Counter([l.split('\t')[0] for l in list(open('data/hightemp.txt'))]).most_common()