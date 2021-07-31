#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
import numpy as np
from collections import Counter
# In[2]:
## Please disregard, just some css for styling
from IPython.display import HTML
HTML("""<style>@import "http://fonts.googleapis.com/css?family=Lato|Source+Code+Pro|Montserrat:400,700";#notebook-container{-webkit-box-shadow:none;box-shadow:none}h1,h2,h3,h4,h5,h6{font-family:'Avenir Next'}h1{font-size:4.5em}h2{font-size:4rem}h3{font-size:3.5rem}h4{font-size:3rem}h5{font-size:2.5rem}h6{font-size:2rem}p{font-family:'Avenir Next';font-size:12pt;line-height:15pt;color:#2F4F4F}.CodeMirror pre{font-family:'Source Code Pro', monospace;font-size:0.95em}div.input_area{border:none;background:whitesmoke}</style>""")
# In[3]:
get_ipython().run_cell_magic('bash', '', 'wc -lw trump.txt')
# In[4]:
## I'm importing functions from the python scripts for use here without copying and pasting
##     all the functions. Please refer to the .py files for the implementations.
from train_markov_chain import get_transition_matrix
from generate_text import simulate_markov_states, get_text
# In[5]:
get_ipython().run_cell_magic('bash', '--out paragraph', 'for i in `seq 1 20000`;\n    do\n        line_string=$(head -$((${RANDOM} % `wc -l < trump.txt` + 1)) trump.txt | tail -1)\n        line_array=($line_string)\n        num_words=${#line_array[*]}\n        echo ${line_array[$((RANDOM%num_words))]}\n    done')
# In[6]:
' '.join(paragraph.split('\n')[:200])
# In[7]:
word_count = Counter(paragraph.split('\n'))
# In[8]:
list(zip(range(1,11), word_count.most_common(10)))
# In[9]:
P = get_transition_matrix('trump.txt', markov_model_order=1)
# In[10]:
P.shape
# In[11]:
P.index
# In[12]:
P.sum(axis=1)[:10]
# In[13]:
print(' '.join(get_text(simulate_markov_states(P, num_states=200))))
# In[14]:
word_count.clear()
word_count.update(get_text(simulate_markov_states(P, num_states=100000)))
# In[15]:
list(zip(range(1,11), word_count.most_common(10)))
# In[16]:
P = get_transition_matrix('trump.txt', markov_model_order=2)
# In[17]:
P.shape
# In[18]:
P.index
# In[19]:
print(' '.join(get_text(simulate_markov_states(P, num_states=200))))
# In[20]:
word_count.clear()
word_count.update(get_text(simulate_markov_states(P, num_states=100000)))
# In[21]:
list(zip(range(1,11), word_count.most_common(10)))
# In[22]:
P = get_transition_matrix('trump.txt', markov_model_order=3)
# In[23]:
P.shape
# In[24]:
print(' '.join(get_text(simulate_markov_states(P, num_states=200))))