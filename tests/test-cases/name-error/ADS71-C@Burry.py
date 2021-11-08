#!/usr/bin/env python
# coding: utf-8
# In[2]:
doc['bericht tekst'] = doc['bericht tekst'].fillna('')
# In[3]:
doc['bericht tekst'] = doc['bericht tekst'].str.lower()
# In[4]:
doc  = doc[~doc['bericht tekst'].str.contains('rt')]
doc  = doc[~doc['bericht tekst'].str.contains(r'http[s]*')]  # TODO secure?
doc  = doc[~doc['auteur'].str.contains('grieptweets')]  # TODO to file
doc  = doc[~doc['auteur'].str.contains('kleenex_helpt')]
# doc.head()
# In[5]:
doc = doc.drop_duplicates()
doc = doc.drop_duplicates(subset='url',keep='first')
len(doc)
# In[6]:
re_clean = re.compile(r'(https?://\S+|@\S+)')
re_words = re.compile(r'(\w+-?\w*)')
def clean_text(text: str):
    words = []
    if text:
        text = re_clean.sub(' ', text)
        words = re_words.findall(text)
    return words
# In[7]:
all_tweets = pd.read_csv('sample_alltweets.csv', sep=';')
all_tweets.head()
# In[8]:
doc['bericht woorden'] = doc['bericht tekst'].map(clean_text)
# In[9]:
all_tweets['bericht tekst'] = all_tweets['bericht tekst'].fillna('')
# In[10]:
all_tweets['bericht tekst'] = all_tweets['bericht tekst'].str.lower()
# In[11]:
all_tweets = all_tweets[~all_tweets['bericht tekst'].str.contains('rt')]
all_tweets.head()
# In[12]:
all_tweets['bericht woorden'] = all_tweets['bericht tekst'].map(clean_text)
# In[13]:
execute_learning = False
# In[14]:
result = []
if execute_learning: 
    counter = Counter()
    for words in all_tweets['bericht woorden']:
        counter.update(words)
    result = counter.most_common(25)
result
# In[15]:
if execute_learning: 
    common_words = set([word[0] for word in counter.most_common(300)])
# In[16]:
if execute_learning: 
    blacklisted_words = set(common_words)
    blacklisted_words.update(set(search_terms))
# In[17]:
related_words = []
if execute_learning: 
    counter = Counter()
    for words in doc['bericht woorden']:
        words = set(words)
        filtered_words = words - blacklisted_words
        counter.update(filtered_words)
    related_words = counter.most_common(25)
related_words
# In[18]:
model = Word2Vec.load('word2vec.model')
# In[20]:
def scorer(row):
    if 'score' not in row:
        score = 0
        words = [word.replace('#', '') for word in row['bericht woorden'] if word in model.wv.vocab]
        if words:
            score = model.wv.n_similarity(sickness_terms, words)
        if row['type'] == 'comment':
            score /= 2
        row['score'] = score
    return row
doc = doc.apply(scorer, axis=1)
doc = doc.sort_values('score', ascending=False)
# In[21]:
pd.set_option('display.max_colwidth', 250)
pd.options.display.max_rows = 999
# In[22]:
doc.filter(items=['bericht tekst',  'score', 'auteur', 'type']).head(250)