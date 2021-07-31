#!/usr/bin/env python
# coding: utf-8
# In[1]:
def pretty_print_review_and_label(i):
    print(labels[i] + "\t:\t" + reviews[i][:80] + "...")
g = open('reviews.txt','r') # What we know!
reviews = list(map(lambda x:x[:-1],g.readlines()))
g.close()
g = open('labels.txt','r') # What we WANT to know!
labels = list(map(lambda x:x[:-1].upper(),g.readlines()))
g.close()
# In[2]:
len(reviews)
# In[3]:
reviews[0]
# In[4]:
labels[0]
# In[5]:
print("labels.txt \t : \t reviews.txt\n")
pretty_print_review_and_label(2137)
pretty_print_review_and_label(12816)
pretty_print_review_and_label(6267)
pretty_print_review_and_label(21934)
pretty_print_review_and_label(5297)
pretty_print_review_and_label(4998)
# In[7]:
from collections import Counter
import numpy as np
# In[8]:
# Create three Counter objects to store positive, negative and total counts
positive_counts = Counter()
negative_counts = Counter()
total_counts = Counter()
# In[10]:
# TODO: Loop over all the words in all the reviews and increment the counts in the appropriate counter objects
for x in range(0, len(reviews)):
    for word in reviews[x].split(' '):        
        if labels[x] == 'POSITIVE':
            positive_counts[word] += 1
        if labels[x] == 'NEGATIVE':
            negative_counts[word] += 1
        total_counts[word] += 1
        
# In[11]:
# Examine the counts of the most common words in positive reviews
positive_counts.most_common()
# In[12]:
# Examine the counts of the most common words in negative reviews
negative_counts.most_common()
# In[13]:
negative_counts['the']
# In[17]:
# Create Counter object to store positive/negative ratios
pos_neg_ratios = Counter()
# TODO: Calculate the ratios of positive and negative uses of the most common words
#       Consider words to be "common" if they've been used at least 100 times
for word in total_counts:
    if total_counts[word] > 100:
        pos_neg_ratios[word] = positive_counts[word] / float(negative_counts[word]+1)
# In[18]:
print("Pos-to-neg ratio for 'the' = {}".format(pos_neg_ratios["the"]))
print("Pos-to-neg ratio for 'amazing' = {}".format(pos_neg_ratios["amazing"]))
print("Pos-to-neg ratio for 'terrible' = {}".format(pos_neg_ratios["terrible"]))
# In[19]:
# TODO: Convert ratios to logs
for word in pos_neg_ratios:
    if pos_neg_ratios[word] > 1:
        pos_neg_ratios[word] = np.log(pos_neg_ratios[word])
    elif pos_neg_ratios[word] < 1:
        pos_neg_ratios[word] =  -np.log(1/(pos_neg_ratios[word] + 0.01))
# In[20]:
print("Pos-to-neg ratio for 'the' = {}".format(pos_neg_ratios["the"]))
print("Pos-to-neg ratio for 'amazing' = {}".format(pos_neg_ratios["amazing"]))
print("Pos-to-neg ratio for 'terrible' = {}".format(pos_neg_ratios["terrible"]))
# In[21]:
# words most frequently seen in a review with a "POSITIVE" label
pos_neg_ratios.most_common()
# In[22]:
# words most frequently seen in a review with a "NEGATIVE" label
list(reversed(pos_neg_ratios.most_common()))[0:30]
# Note: Above is the code Andrew uses in his solution video, 
#       so we've included it here to avoid confusion.
#       If you explore the documentation for the Counter class, 
#       you will see you could also find the 30 least common
#       words like this: pos_neg_ratios.most_common()[:-31:-1]
# In[1]:
from IPython.display import Image
Image(filename='sentiment_network_2.png')