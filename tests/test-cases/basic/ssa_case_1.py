# Imports
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
# Set environment variable
# Geonames requires a username to access the API but we do not want to expose personal info in code
#
# Run this locally by adding USERNAME to environment variables, e.g. to .env, as follows:
# > export USERNAME=<insert username here>
USERNAME = os.getenv('USERNAME')
# Setup Stanford NER Tagger
# Ignore deprecation warning for now; we'll deal with it when the time comes!
st = StanfordNERTagger('/usr/local/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', 
                       '/usr/local/share/stanford-ner/stanford-ner.jar',
                       encoding='utf-8')
# Functions for putting together with inside-outside-beginning (IOB) logic
# Cf. https://stackoverflow.com/a/30666949
#
# For more information on IOB tagging, see https://en.wikipedia.org/wiki/Inside–outside–beginning_(tagging)
def stanfordNE2BIO(tagged_sent):
    bio_tagged_sent = []
    prev_tag = "O"
    for token, tag in tagged_sent:
        if tag == "O": #O
            bio_tagged_sent.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O": # Begin NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag: # Inside NE
            bio_tagged_sent.append((token, "I-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag
    return bio_tagged_sent
def stanfordNE2tree(ne_tagged_sent):
    bio_tagged_sent = stanfordNE2BIO(ne_tagged_sent)
    sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
    sent_pos_tags = [pos for token, pos in pos_tag(sent_tokens)]
    sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
    ne_tree = conlltags2tree(sent_conlltags)
    return ne_tree
# Sample HathiTrust ID
# This is the HTID for... 
# "Ancient Corinth: A guide to the excavations," O. Broneer, R. Carpenter, and C. H. Morgan
htid = "wu.89079728994"
# Get HTEF data for this ID; specifically tokenlist
fr = FeatureReader(ids=[htid])
for vol in fr:
    tokens = vol.tokenlist()
# Create pandas dataframe with relevant data
temp = tokens.index.values.tolist()
counts = pd.DataFrame.from_records(temp, columns=['page', 'section', 'token', 'pos'])
counts['count'] = tokens['count'].tolist()
counts[:10]
# Reconstruct text using tokens and counts
text_data = list(zip(counts['token'].tolist(), counts['count'].tolist()))
# Loop through and multiply words by counts
text_list = []
for w, c in text_data:
    for i in range(0, c):
        text_list.append(w)
random.shuffle(text_list) # Necessary?
text_reconstruction = " ".join(text_list)
#page_words_extended = page_words+page_ner
tokens = word_tokenize(text_reconstruction)
tagged_tokens = st.tag(tokens)
tagged_tokens = [item for item in tagged_tokens if item[0] != '']
