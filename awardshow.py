import nltk, json

with open('goldenglobes.json', 'r') as f:
     tweets = map(json.loads, f)
# tweet_txt_array = []
# for tweet in tweets:
# 	tweet_txt_array.append(tweet['text'])

def get_dict_buckets():
	text_file = open("dict_buckets.txt", "r")
	lines = text_file.readlines()
	buckets = []
	for line in lines:
		 buckets.append(line.rstrip())
	return buckets

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

	print hosts
	return hosts
	# return people
main()