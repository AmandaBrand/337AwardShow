import nltk, json, re

with open('goldenglobes.json', 'r') as f:
     tweets = map(json.loads, f)
# tweet_txt_array = []
# for tweet in tweets:
# 	tweet_txt_array.append(tweet['text'])

def clean(tweet):
	tweet = tweet.replace("RT @goldenglobes: ","")
	tweet = tweet.replace("- #GoldenG","").replace("- #GoldenGlobes","").replace("lobes","")
	tweet =  re.sub(r'\(@.+\)', "", tweet)
	tweet =  re.sub(r'#.+', "", tweet)
	tweet =  re.sub(r'\"$', "", tweet)
	tweet =  re.sub(r'http\:\/\/t\.co\/.+', "", tweet)
	tweet =  re.sub(r'\/\/.+.+', "", tweet)
	tweet =  re.sub(r'\".+\"', "", tweet)
	tweet =  re.sub(r'-\s+-', "-", tweet)
	tweet = tweet.replace("&amp;","and")

	# tweet =  re.sub(r'.+', "", tweet)
	return tweet

def get_dict_buckets():
	text_file = open("dict_buckets.txt", "r")
	lines = text_file.readlines()
	buckets = []
	for line in lines:
		 buckets.append(line.rstrip())
	return buckets

def find_hosts(host_tweets):
	name_array = []
	count_array = []
	for tweet in host_tweets:
		people = person_search(tweet)
		if len(people):
			for person in people:
				if person in name_array:
					index = name_array.index(person)
					count_array[index] = count_array[index] + 1
				else:
					name_array.append(person)
					count_array.append(1)
	##get top 2
	sorted_counts = sorted(count_array)
	most = sorted_counts[-1]
	second_most = sorted_counts[-2]
	most_index = count_array.index(most)
	second_index = count_array.index(second_most)

	return name_array[most_index], name_array[second_index]

## Currently, I can only get the functions to work by copying these definitions into
## the command line and running them there 
def person_search(text):
	"Takes a piece of text, pulling out people names"
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	namecorpus = nltk.corpus.names
	names = namecorpus.words('male.txt')
	names.extend(namecorpus.words('female.txt'))
	sentences = sent_detector.tokenize(text)
	entities = []
	stoplist = ["Justin REALLY", "Clinton Endorses"]
	for sentence in sentences:
		temp = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))
		for entity in temp:
			try:
				nodeLabel = entity.node;
			except AttributeError:
				pass
			else:
				if (nodeLabel=='PERSON' and len(entity)==2 and entity[0][0] in names):
					person = entity[0][0]+" "+entity[1][0]
					if (person in stoplist):
						pass
					else:
						entities.append(person)
	return entities

def find_winners():
	print "--WINNERS--"
	already_seen = [] #will hold hashes of tweets so we don't print the same tweet twice
	cecil_award = []
	for tweet in tweets:
		temp_array = [] #holds split tweet (i.e. ["Best Actor", "Russell Crowe", "Les Miserable"])
		tweet_text = tweet["text"]

		if "RT @goldenglobes: Best" in tweet_text:
			tweet_text = clean(tweet_text)

			if "RT" not in tweet_text and "+" not in tweet_text:##more cleaning

				temp_array = tweet_text.split("-")#the tweets look like "Best Actor - Russell Crowe - Les Miserable"

				if hash(tweet_text.lower().replace(" ","")) not in already_seen and "Best" == temp_array[0][:4]:
				#first part, checking if we have seen it before
				#second part is just cleaning out tweets that don't start with "Best"
					already_seen.append(hash(tweet_text.lower().replace(" ","")))
					length = len(temp_array)
					#different formats of tweets based on how many "-" are included in the tweet
					if length == 3:
						#[award, winner, movie]
						print temp_array[0] + "- "+temp_array[1] +"- " +temp_array[2]
					if length == 4:
						#[award, category, winer, movie ]
						print temp_array[0]+ "- " +temp_array[1]+ "- "+temp_array[2] +"- "+temp_array[3]
					if length == 2:
						#[award, winner]
						print temp_array[0] + "- "+temp_array[1]
		if "Cecil" in tweet_text:
			cecil_award.append(tweet_text)
	print "Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures - " + find_hosts(cecil_award)[0]
	print ""


#makes a dictionary with buckets dictated in dict_buckets.txt
def make_tweet_dict():
	dict_buckets = get_dict_buckets()
	tweets_dict = {}
	for tweet in tweets:
		for bucket in dict_buckets:
			tweet_text = tweet['text']
			if bucket in tweet_text:
				if bucket in tweets_dict.keys():
					tweets_dict[bucket].append(tweet_text)
				else:
					#if a tweet for that bucket hasn't been stored yet, start the array
					tweets_dict[bucket] = [tweet_text]
	return tweets_dict

def find_hosts(host_tweets):
	name_array = []
	count_array = []
	for tweet in host_tweets:
		people = person_search(tweet)
		if len(people):
			for person in people:
				if person in name_array:
					index = name_array.index(person)
					count_array[index] = count_array[index] + 1
				else:
					name_array.append(person)
					count_array.append(1)
	##get top 2
	sorted_counts = sorted(count_array)
	most = sorted_counts[-1]
	second_most = sorted_counts[-2]
	most_index = count_array.index(most)
	second_index = count_array.index(second_most)

	return name_array[most_index], name_array[second_index]

def main():
	tweet_dict = make_tweet_dict()

	hosts = find_hosts(tweet_dict['hosted'])
	find_winners()

	print hosts
	return hosts
	# return people
main()