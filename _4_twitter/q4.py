from _4_twitter.TwitterConnector import TwitterConnector
from DBConnector import GetCursor

url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params = {"count": 10}

values = []
for tweet in TwitterConnector().get_json_req(url, params):
    values.append((tweet['id_str'], tweet['user']['name'], tweet['text']))

insert = 'INSERT INTO `lab`.`bow2` (`kiji`, `genkei`, `hinshi`) VALUES (%s, %s, %s)'
with GetCursor() as cur:
    cur.executemany()
