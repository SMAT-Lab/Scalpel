import pymongo
from collections import Counter
import pprint
pp = pprint.PrettyPrinter(indent=4)
c = pymongo.MongoClient('mongodb://mongodb:27017')
db = c['public_wpdocs']
fp = db['full_pages']
litems = [dict(item=item['url'],
               links=[x for x in item['links'] if 'https://' in x],
               content_links=[x for x in item['content_links']])
          for item in fp.find()]
pp.pprint(litems[0])
link_list = [link for links in [item['links'] for item in litems] for link in links]
c = Counter(link_list)
pp.pprint(c)
clink_list = [link for links in [item['content_links'] for item in litems] for link in links]
c = Counter(clink_list)
pp.pprint(c)