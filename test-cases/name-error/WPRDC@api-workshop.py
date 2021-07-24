#!/usr/bin/env python
# coding: utf-8
# In[1]:
import json
from datetime import datetime, timedelta
import requests
import tweepy
# In[3]:
wprdc_api_endpoint = "https://data.wprdc.org/api/3/action/datastore_search_sql"
# In[8]:
resource_id = "1797ead8-8262-41cc-9099-cbc8a161924b"
# In[16]:
# Get yesterday's date (the current date - 1 day)
yesterday_date = datetime.now() - timedelta(days=1)
yesterday_date
# In[19]:
query = "SELECT count(\"PK\") as count FROM \"{}\" WHERE \"INCIDENTTIME\" >= '{}';".format(resource_id, yesterday_str)
query
# In[26]:
response = requests.get(wprdc_api_endpoint, {'sql': query})
response
# In[27]:
response.text
# In[28]:
response_data = json.loads(response.text)
response_data
# In[34]:
print(json.dumps(response_data, sort_keys=True, indent=2, separators=(',', ': ')))  # just to demonstrate the JSON format - not required
# In[33]:
count = response_data['result']['records'][0]['count']
count
# In[36]:
with open('twitter_keys_sample.json') as f:
    twitter_keys = json.load(f)
    
print(json.dumps(twitter_keys, sort_keys=True, indent = 2, separators=(',', ': ')))
# In[37]:
with open('twitter_keys.json') as f:
    twitter_keys = json.load(f)
# In[38]:
consumer_key = twitter_keys['consumer_key']
consumer_secret = twitter_keys['consumer_secret']
access_token_key = twitter_keys['access_token_key']
access_token_secret = twitter_keys['access_token_secret']
# In[39]:
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
# In[45]:
twitter = tweepy.API(auth)
twitter
# In[46]:
twitter.update_status('Gee willickers! There were {} crime incidents in Pittsburgh yesterday.'.format(count))