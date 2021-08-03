import os
import random
from collections import Counter, defaultdict
import random
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
import pandas as pd
from htrc_features import FeatureReader
import geocoder
import folium
from pprint import pprint
from tqdm import tqdm
USERNAME = os.getenv('USERNAME')
st = StanfordNERTagger(
    '/usr/local/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz'
    , '/usr/local/share/stanford-ner/stanford-ner.jar', encoding='utf-8')


def stanfordNE2BIO(tagged_sent):
    bio_tagged_sent = []
    prev_tag = 'O'
    for token, tag in tagged_sent:
        if tag == 'O':
            bio_tagged_sent.append((token, tag))
            prev_tag = tag
            continue
        if tag != 'O' and prev_tag == 'O':
            bio_tagged_sent.append((token, 'B-' + tag))
            prev_tag = tag
        elif prev_tag != 'O' and prev_tag == tag:
            bio_tagged_sent.append((token, 'I-' + tag))
            prev_tag = tag
        elif prev_tag != 'O' and prev_tag != tag:
            bio_tagged_sent.append((token, 'B-' + tag))
            prev_tag = tag
    return bio_tagged_sent


def stanfordNE2tree(ne_tagged_sent):
    bio_tagged_sent = stanfordNE2BIO(ne_tagged_sent)
    sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
    _hidden_sent_pos_tags = 
    []
    for token, pos in pos_tag(sent_tokens):
        _hidden_sent_pos_tags.append(pos)
    token, pos = _hidden_sent_pos_tags
    _hidden_sent_conlltags = 
    []
    for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags):
        _hidden_sent_conlltags.append((token, pos, ne))
    token, pos, ne = _hidden_sent_conlltags
    ne_tree = conlltags2tree(sent_conlltags)
    return ne_tree


htid = 'wu.89079728994'
fr = FeatureReader(ids=[htid])
for vol in fr:
    tokens = vol.tokenlist()
temp = tokens.index.values.tolist()
counts = pd.DataFrame.from_records(temp, columns=['page', 'section',
    'token', 'pos'])
counts['count'] = tokens['count'].tolist()
counts[:10]
text_data = list(zip(counts['token'].tolist(), counts['count'].tolist()))
text_list = []
for w, c in text_data:
    for i in range(0, c):
        text_list.append(w)
random.shuffle(text_list)
text_reconstruction = ' '.join(text_list)
tokens = word_tokenize(text_reconstruction)
tagged_tokens = st.tag(tokens)
_hidden_tagged_tokens = 
[]
for item in tagged_tokens:
    if item[0] != '':
        _hidden_tagged_tokens.append(item)
item = _hidden_tagged_tokens

