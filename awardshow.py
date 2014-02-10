import nltk, json

with open('/Users/williamgross/337AwardShow/goldenglobes.json', 'r') as f:
     tweets = map(json.loads, f)

tweet_txt_array = []
for tweet in tweets:
	tweet_txt_array.append(tweet['text'])

## Currently, I can only get the functions to work by copying these definitions into
## the command line and running them there 
def person_search(text):
	"Takes a piece of text, pulling out people names"
	import nltk
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = sent_detector.tokenize(text)
	tokens = []
	tags = []
	entities = []
	for sentence in sentences:
		temp = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))
		for entity in temp:
			try:
				nodeLabel = entity.node;
			except AttributeError:
				pass
			else:
				if (nodeLabel=='PERSON' and len(entity)==2):
					person = entity[0][0]+" "+entity[1][0]
					entities.append(person)
	return entities

def looped_search(tweets):
	"Loops through tweets and exports people found in them as a list"
	people = [];
	for tweet in tweets:
		temp = person_search(tweet['text'])
		if temp!=[]:
			people.append(temp)
	return people