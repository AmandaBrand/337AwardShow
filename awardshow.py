import nltk, json

with open('goldenglobes.json', 'r') as f:
     tweets = map(json.loads, f)
# tweet_txt_array = []
# for tweet in tweets:
# 	tweet_txt_array.append(tweet['text'])
def clean(tweet):
	tweet = tweet.replace("RT @goldenglobes: ","")
	tweet = tweet.replace("- #GoldenG","").replace("- #GoldenGlobes","").replace("lobes","")
	return tweet
def loop():
	already_seen = []
	for tweet in tweets:
		temp_array = []
		tweet_text = tweet["text"]
		if "RT @goldenglobes: Best" in tweet_text:
			tweet_text = clean(tweet_text)
			if "RT" not in tweet_text:##more cleaning
				temp_array = tweet_text.split("-")

				#second part of this if is to get out a lot of RT's of "goldenglobe"
				if hash(tweet_text) not in already_seen and "Best" == temp_array[0][:4]:

					already_seen.append(hash(tweet_text))
					temp_array = tweet_text.split("-")
					length = len(temp_array)
					if length == 3:
						#[award, winner, movie]
						print temp_array[1] + "wins " +temp_array[0] + "in " +temp_array[2]
					if length == 4:
						#[award, category, winer, movie ]
						print temp_array[2]+"wins "+temp_array[0]+ "-" +temp_array[1]+ "in "+temp_array[3]
					if length == 2:
						#[award, winner]
						print temp_array[1] + "wins "+temp_array[0]
					print ""

loop()

