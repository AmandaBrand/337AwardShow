import nltk, json

with open('goldenglobes.json', 'r') as f:
     tweets = map(json.loads, f)

tweet_txt_array = []
for tweet in tweets:
	tweet_txt_array.append(tweet['text'])

print tweet_txt_array
