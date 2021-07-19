import json
from datetime import datetime, timedelta
import requests
import tweepy
wprdc_api_endpoint = "https://data.wprdc.org/api/3/action/datastore_search_sql"
resource_id = "1797ead8-8262-41cc-9099-cbc8a161924b"
# Get yesterday's date (the current date - 1 day)
yesterday_date = datetime.now() - timedelta(days=1)
yesterday_date
# Convert to a string format that the Data Center accepts (yyyy-mm-dd)
yesterday_str = yesterday_date.strftime("%Y-%m-%d")
yesterday_str
query = "SELECT count(\"PK\") as count FROM \"{}\" WHERE \"INCIDENTTIME\" >= '{}';".format(resource_id, yesterday_str)
query
response = requests.get(wprdc_api_endpoint, {'sql': query})
response
response.text
response_data = json.loads(response.text)
response_data
print(json.dumps(response_data, sort_keys=True, indent=2, separators=(',', ': ')))  # just to demonstrate the JSON format - not required
count = response_data['result']['records'][0]['count']
count
with open('twitter_keys_sample.json') as f:
    twitter_keys = json.load(f)
    
print(json.dumps(twitter_keys, sort_keys=True, indent = 2, separators=(',', ': ')))
with open('twitter_keys.json') as f:
    twitter_keys = json.load(f)
consumer_key = twitter_keys['consumer_key']
consumer_secret = twitter_keys['consumer_secret']
access_token_key = twitter_keys['access_token_key']
access_token_secret = twitter_keys['access_token_secret']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
twitter = tweepy.API(auth)
twitter
twitter.update_status('Gee willickers! There were {} crime incidents in Pittsburgh yesterday.'.format(count))