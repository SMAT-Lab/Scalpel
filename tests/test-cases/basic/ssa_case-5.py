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
ne_tree = stanfordNE2tree(tagged_tokens)
ne_in_sent = []
for subtree in ne_tree:
    if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
        ne_label = subtree.label()
        ne_string = " ".join([token for token, pos in subtree.leaves()])
        ne_in_sent.append((ne_string, ne_label))
    
locations = [tag[0].title() for tag in ne_in_sent if tag[1] == 'LOCATION']
print(locations)
most_common_locations = Counter(locations).most_common(10)
pprint(most_common_locations)
# Organize some data for map info
places_list = [name for name, _ in most_common_locations][:3] # Limit to top three
most_common_locations = dict(most_common_locations) # Turn mcl into dictionary
# Retrieve json from geonames API (for fun this time using geocoder)
geocoder_results = []
for place in places_list:
    results = geocoder.geonames(place, maxRows=5, key=USERNAME)
    jsons = []
    for result in results:
        jsons.append(result.json)
    geocoder_results.append(jsons)
# Create a list of 'country' from the geonames json results
countries = []
for results in geocoder_results:
    for item in results:
        if 'country' in item.keys():
            countries.append(item['country'])
# Determine which country appears most often
top_country = sorted(Counter(countries))[0]
print(top_country)
# Iterate over geocoder_results and keep the first lat/long that matches the top country
coordinates = []
for i, results in enumerate(geocoder_results):
    for item in results:
        if item['country'] == top_country:
            coordinates.append((float(item['lat']), float(item['lng'])))
            break # Only get the first item for now
print(places_list)            
print(coordinates)
# Set up Folium and populate with weighted coordinates
basemap = folium.Map(location=[37.97945, 23.71622], zoom_start=8, tiles='cartodbpositron', width=960, height=512)
for i, c in enumerate(coordinates):
    folium.CircleMarker([c[0], c[1]], radius=most_common_locations[places_list[i]]*.25, color='#3186cc',
                    fill=True, fill_opacity=0.5, fill_color='#3186cc', 
                    popup='{} ({}, {}) appears {} times in book.'.format(places_list[i], c[0], c[1], most_common_locations[places_list[i]])).add_to(basemap)
print('Map of relevant locations in Broneer et al.\'s "Ancient Corinth: A guide to the excavations," weighted by frequency.')
basemap
page = 87
test = counts[counts['page'] == page]['token'].tolist()
print(test)
print(len(test))
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))
pns_list = []
for i in range(1, max(counts['page'])+1):
    tokens = counts[counts['page'] == i]['token'].tolist()
    tokens = [token for token in tokens if token.lower() not in stops and len(token) > 2]
    pns = [token for token in tokens if token[0].isupper()]
    combs = [f'{x} {y}' for x, y in combinations(pns, 2)]
    pns_list.extend(combs)
