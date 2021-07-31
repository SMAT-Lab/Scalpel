#!/usr/bin/env python
# coding: utf-8
# In[1]:
# let's import an RSS feed package
import feedparser
# In[2]:
# we'll start by parsing Up First and see what we get
feed = feedparser.parse('https://www.npr.org/rss/podcast.php?id=510318')
print(feed)
# In[3]:
feed.keys()
# In[4]:
import json
# In[5]:
print(json.dumps(feed['entries'], sort_keys=True, indent=2))
# In[6]:
print(json.dumps(feed['feed'], sort_keys=True, indent=2))
# In[7]:
# podcast name
print(feed['feed']['title'])
# In[8]:
# release date
print(feed['feed']['updated'])
# In[9]:
# show description
print(feed['entries'][0]['content'][0]['value'])
# In[10]:
# mp3 URL
print(feed['entries'][0]['links'][0]['href'])
# In[11]:
import urllib
# In[12]:
podcast_url = feed['entries'][0]['links'][0]['href']
# In[13]:
urllib.request.urlretrieve(podcast_url, 'upfirst_10_04_2017.mp3')
# In[14]:
# create an empty dict to store IDs and podcast names
npr_podcasts = {}
for i in range(510300, 510400):
    try:
        feed = feedparser.parse('https://www.npr.org/rss/podcast.php?id={}'.format(str(i)))
        # store the podcast name as the key, as it's easier to search
        npr_podcasts[feed.feed.title] = i
    except:
        pass
print(npr_podcasts)
# In[15]:
import pygame
# In[16]:
# create a function that plays mp3 files 
# but also handles the asynchronous nature of pygame.mixer
def play(podcast):
    pygame.init()
    pygame.mixer.music.load('archive/{}/{}.mp3'.format(podcast_name, podcast))
    pygame.mixer.music.play(0)
    
    clock = pygame.time.Clock()
    clock.tick(10)
    
    while pygame.mixer.music.get_busy():
        pygame.event.poll()
        clock.tick(10)
    