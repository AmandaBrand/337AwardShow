import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

with open('goldenglobes.json', 'r') as f:
     tweets = map(json.loads, f)

f = open('tweets.txt','w')

for tweet in tweets:
	text = tweet["text"]
	f.write(text+"\n")
f.close()