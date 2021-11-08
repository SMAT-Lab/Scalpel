#!/usr/bin/env python
# coding: utf-8
# In[1]:
import twitter
# In[2]:
# Define your api_key/secret and access_token_key/secret here
api = twitter.Api(consumer_key=api_key,
                      consumer_secret=api_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
# In[3]:
api.VerifyCredentials()
# In[4]:
def get_statuses(prev_statuses = None, screen_name = "realDonaldTrump", count=200):
    max_id = prev_statuses[-1].id-1 if prev_statuses else None
    return api.GetUserTimeline(screen_name=screen_name, max_id=max_id, count=count)
# In[5]:
n = 16
temp = get_statuses()
all_statuses = temp
for _ in range(n):
    temp = get_statuses(temp)
    all_statuses += temp
# In[6]:
# Earliest tweet scraped
all_statuses[-1]
# In[7]:
#https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
import datetime
def readable_date(unix_time):
    return datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y.%m.%d')
# In[8]:
text_and_date = [(status.text, readable_date(status.created_at_in_seconds)) for status in all_statuses]
# In[9]:
# Most recent tweet
text_and_date[0]
# In[10]:
def trim_results(text_and_date, filterx):
    return list(filter(
        lambda y: len(y[1]) > 0,
        [(date, 
            " ".join(filter(filterx, 
                            map(lambda x: x.replace('-', ' ').replace(u'\u2026', '').strip(), 
                                text.strip().split())
            ))
        ) for (text, date) in text_and_date]
    ))
# In[11]:
filter1 = lambda x: x != u'&amp;' and (len(x) > 0 and x[0].upper() == x[0] 
                   or x.upper() == x or u'#' == x[0] or u'!' == x[-1])
# In[12]:
trimmed1 = trim_results(text_and_date, filter1)
# In[13]:
trimmed1[:20]
# In[14]:
#https://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
def IsASCII(u):
    try: 
        u.encode()
        return True
    except UnicodeEncodeError:
        return False
# In[15]:
filter2 = lambda x: x.upper() == x and not RepresentsInt(x) and u'-' != x and x != u'RT' and len(x) > 3 and IsASCII(x)
# In[16]:
trimmed2 = trim_results(text_and_date, filter2)
# In[17]:
trimmed2[:20]
# In[18]:
from collections import Counter
# In[19]:
trump_yelling = Counter([x[1] for x in trimmed2])
# In[20]:
[i for i in trump_yelling.most_common() if i[1] > 2]
# In[21]:
sorted(trump_yelling.keys())
# In[22]:
get_ipython().run_line_magic('store', 'all_statuses > all_statuses.txt')
get_ipython().run_line_magic('store', 'text_and_date > text_and_date.txt')
get_ipython().run_line_magic('store', 'trimmed1 > trimmed1.txt')
get_ipython().run_line_magic('store', 'trimmed2 > trimmed2.txt')
get_ipython().run_line_magic('store', 'trump_yelling > trump_yelling.txt')
# In[23]:
get_ipython().run_line_magic('store', '-r')