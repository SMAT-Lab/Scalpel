#!/usr/bin/env python
# coding: utf-8
# In[3]:
# Get first token of the processed document
token = doc[0]
print(token)
# Print sentences (one sentence per line)
for sent in doc.sents:
    print(sent)
# In[5]:
# Print all named entities with named entity types
doc_2 = nlp(u"I went to Paris where I met my old friend Jack from uni.")
for ent in doc_2.ents:
    print('{} - {}'.format(ent, ent.label_))
# In[6]:
# Print noun chunks for doc_2
print([chunk for chunk in doc_2.noun_chunks])