import twitter
# Define your api_key/secret and access_token_key/secret here
api = twitter.Api(consumer_key=api_key,
                      consumer_secret=api_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
api.VerifyCredentials()
def get_statuses(prev_statuses = None, screen_name = "realDonaldTrump", count=200):
    max_id = prev_statuses[-1].id-1 if prev_statuses else None
    return api.GetUserTimeline(screen_name=screen_name, max_id=max_id, count=count)
n = 16
temp = get_statuses()
all_statuses = temp
for _ in range(n):
    temp = get_statuses(temp)
    all_statuses += temp
# Earliest tweet scraped
all_statuses[-1]
#https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
import datetime
def readable_date(unix_time):
    return datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y.%m.%d')
text_and_date = [(status.text, readable_date(status.created_at_in_seconds)) for status in all_statuses]
# Most recent tweet
text_and_date[0]
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
filter1 = lambda x: x != u'&amp;' and (len(x) > 0 and x[0].upper() == x[0] 
                   or x.upper() == x or u'#' == x[0] or u'!' == x[-1])
trimmed1 = trim_results(text_and_date, filter1)
trimmed1[:20]
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
filter2 = lambda x: x.upper() == x and not RepresentsInt(x) and u'-' != x and x != u'RT' and len(x) > 3 and IsASCII(x)
trimmed2 = trim_results(text_and_date, filter2)
trimmed2[:20]
from collections import Counter
trump_yelling = Counter([x[1] for x in trimmed2])
[i for i in trump_yelling.most_common() if i[1] > 2]
sorted(trump_yelling.keys())