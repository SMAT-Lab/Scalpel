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
    _hidden_sent_pos_tags = []
    for token, pos in pos_tag(sent_tokens):
        _hidden_sent_pos_tags.append(pos)
    sent_pos_tags = _hidden_sent_pos_tags
    _hidden_sent_conlltags = []
    for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags):
        _hidden_sent_conlltags.append((token, pos, ne))
    sent_conlltags = _hidden_sent_conlltags
    ne_tree = conlltags2tree(sent_conlltags)
    return ne_tree

########### example

htid = 'wu.89079728994'
fr = FeatureReader(ids=[htid])
for vol in fr:
    tokens = vol.tokenlist()
temp = tokens.index.values.tolist()

########################


counts = pd.DataFrame.from_records(temp, columns=['page', 'section',
    'token', 'pos'])
counts['count'] = tokens['count'].tolist()
counts[:10]
_hidden_res_71_17 = zip(counts['token'].tolist(), counts['count'].tolist())
text_data = list(_hidden_res_71_17)
text_list = []
for w, c in text_data:
    for i in range(0, c):
        text_list.append(w)
random.shuffle(text_list)
text_reconstruction = ' '.join(text_list)
tokens = word_tokenize(text_reconstruction)
tagged_tokens = st.tag(tokens)
_hidden_tagged_tokens = []
for item in tagged_tokens:
    if item[0] != '':
        _hidden_tagged_tokens.append(item)
tagged_tokens = _hidden_tagged_tokens
ne_tree = stanfordNE2tree(tagged_tokens)
ne_in_sent = []
for subtree in ne_tree:
    if type(subtree) == Tree:
        ne_label = subtree.label()
        _hidden_res_88_29 = []
        for token, pos in subtree.leaves():
            _hidden_res_88_29.append(token)
        ne_string = ' '.join(_hidden_res_88_29)
        ne_in_sent.append((ne_string, ne_label))
_hidden_locations = []
for tag in ne_in_sent:
    if tag[1] == 'LOCATION':
        _hidden_locations.append(tag[0].title())
locations = _hidden_locations
print(locations)
most_common_locations = Counter(locations).most_common(10)
pprint(most_common_locations)
_hidden_places_list = []
for name, _ in most_common_locations:
    _hidden_places_list.append(name)
places_list = _hidden_places_list[:3]
most_common_locations = dict(most_common_locations)
geocoder_results = []
for place in places_list:
    results = geocoder.geonames(place, maxRows=5, key=USERNAME)
    jsons = []
    for result in results:
        jsons.append(result.json)
    geocoder_results.append(jsons)
countries = []
for results in geocoder_results:
    for item in results:
        if 'country' in item.keys():
            countries.append(item['country'])
top_country = sorted(Counter(countries))[0]
print(top_country)
coordinates = []
for i, results in enumerate(geocoder_results):
    for item in results:
        if item['country'] == top_country:
            coordinates.append((float(item['lat']), float(item['lng'])))
            break
print(places_list)
print(coordinates)
basemap = folium.Map(location=[37.97945, 23.71622], zoom_start=8, tiles=
    'cartodbpositron', width=960, height=512)
for i, c in enumerate(coordinates):
    folium.CircleMarker([c[0], c[1]], radius=most_common_locations[
        places_list[i]] * 0.25, color='#3186cc', fill=True, fill_opacity=
        0.5, fill_color='#3186cc', popup=
        '{} ({}, {}) appears {} times in book.'.format(places_list[i], c[0],
        c[1], most_common_locations[places_list[i]])).add_to(basemap)
print(
    'Map of relevant locations in Broneer et al.\'s "Ancient Corinth: A guide to the excavations," weighted by frequency.'
    )
basemap
page = 87
test = counts[counts['page'] == page]['token'].tolist()
print(test)
print(len(test))
from nltk.corpus import stopwords
_hidden_res_137_12 = stopwords.words('english')
stops = set(_hidden_res_137_12)
pns_list = []
for i in range(1, max(counts['page']) + 1):
    tokens = counts[counts['page'] == i]['token'].tolist()
    _hidden_tokens = []
    for token in tokens:
        if token.lower() not in stops and len(token) > 2:
            _hidden_tokens.append(token)
    tokens = _hidden_tokens
    _hidden_pns = []
    for token in tokens:
        if token[0].isupper():
            _hidden_pns.append(token)
    pns = _hidden_pns
    _hidden_combs = []
    for x, y in combinations(pns, 2):
        _hidden_combs.append(f'{x} {y}')
    combs = _hidden_combs
    pns_list.extend(combs)
print([x for x, y in Counter(pns_list).most_common(25)])
geocoder_results = []
for place in pns_list[:15]:
    results = geocoder.geonames(place, maxRows=5, key=USERNAME)
    jsons = []
    for result in results:
        jsons.append(result.json)
    geocoder_results.append(jsons)
geocoder_results
results = geocoder.geonames('Roman Forum', maxRows=5, key=USERNAME)
print(next(result.address for result in results))
g = geocoder.google('Al-Fayum')
print(g.latlng)
coordinates = [g.latlng]
basemap = folium.Map(location=[37.97945, 23.71622], zoom_start=8, tiles=
    'cartodbpositron', width=960, height=512)
for i, c in enumerate(coordinates):
    folium.CircleMarker([c[0], c[1]], radius=most_common_locations[
        places_list[i]] * 0.25, color='#3186cc', fill=True, fill_opacity=
        0.5, fill_color='#3186cc').add_to(basemap)
basemap
_hidden_test = []
for x, y in Counter(pns_list).most_common(10):
    _hidden_test.append(x)
test = _hidden_test
places = []
coordinates = []
for item in test:
    g = geocoder.google(item)
    if g:
        places.append(g.address)
        print(g.address)
        coordinates.append(g.latlng)
basemap = folium.Map(location=[37.97945, 23.71622], zoom_start=8, tiles=
    'cartodbpositron', width=960, height=512)
for i, c in enumerate(coordinates):
    folium.CircleMarker([c[0], c[1]], color='#3186cc', fill=True,
        fill_opacity=0.5, fill_color='#3186cc').add_to(basemap)
basemap

