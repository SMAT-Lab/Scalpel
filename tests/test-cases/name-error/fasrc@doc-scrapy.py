#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().system('pip install pymongo')
# In[2]:
c = pymongo.MongoClient('mongodb://mongodb:27017')
db = c['public_wpdocs']
fp = db['full_pages']
# In[3]:
litems = [dict(item=item['url'],
               links=[x for x in item['links'] if 'https://' in x],
               content_links=[x for x in item['content_links']])
          for item in fp.find()]
# In[4]:
pp.pprint(litems[0])
# In[5]:
link_list = [link for links in [item['links'] for item in litems] for link in links]
# In[8]:
c = Counter(link_list)
pp.pprint(c)
# In[10]:
clink_list = [link for links in [item['content_links'] for item in litems] for link in links]
# In[11]:
c = Counter(clink_list)
pp.pprint(c)