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
	already_seen = [] #will hold hashes of tweets so we don't print the same tweet twice

	for tweet in tweets:
		temp_array = [] #holds split tweet (i.e. ["Best Actor", "Russell Crowe", "Les Miserable"])
		tweet_text = tweet["text"]

		if "RT @goldenglobes: Best" in tweet_text:
			tweet_text = clean(tweet_text)

			if "RT" not in tweet_text:##more cleaning

				temp_array = tweet_text.split("-")#the tweets look like "Best Actor - Russell Crowe - Les Miserable"

				if hash(tweet_text) not in already_seen and "Best" == temp_array[0][:4]:
				#first part, checking if we have seen it before
				#second part is just cleaning out tweets that don't start with "Best"

					already_seen.append(hash(tweet_text))
					length = len(temp_array)
					#different formats of tweets based on how many "-" are included in the tweet
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

