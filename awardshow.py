import nltk, json, re, numpy, feelings

with open('goldenglobes.json', 'r') as f:
     tweets = map(json.loads, f)

winners_lower = []
hosts_lower = []
presenters_lower = []
random_lower = ["oscarsnub", "lewisbest", "jessicachas", "lesmiz", "christophwatlz", "lesmis", "lewislincoln", "ben*boston", "sarapalin", "jobanne", "benafleck"]
# tweet_txt_array = []
# for tweet in tweets:
# 	tweet_txt_array.append(tweet['text'])
award_mapping = {'Best Drama': 'Best Motion Picture - Drama',
	'Best TV Drama': 'Best Television Series - Drama',
	'Animated': 'Best Animated Feature Film',
	'Best Supporting Actor': 'Best Supporting Actor in a Motion Picture',
	'Best Director': 'Best Director',
	'Best Original Song': 'Best Original Song',
	'Best Original Score': 'Best Original Score',
	'Best Screenplay': 'Best Screenplay',
	'Best Supporting Actress in a Motion Picture': 'Best Supporting Actress in a Motion Picture',
	'Best Actor': 'Best Actor in a Motion Picture - Drama',
	'TV actor': 'Best Actor in a TV Movie or Miniseries',
	'foreign': 'Best Foreign Film',
	'TV actress': 'Best Actress in a TV Movie or Miniseries',
	'miniseries': 'Best Miniseries or Motion Picture Made for Television',
	'Best Actress Drama': 'Best Actress in a Motion Picture - Drama',
	'TV comedy': 'Best Television Series - Comedy or Musical',
	'musical or comedy': 'Best Motion Picture - Comedy or Musical',
	'actor in a comedy': 'Best Actor in a Motion Picture - Comedy or Musical',
	'actress in a comedy': 'Best Actress in a Motion Picture - Comedy or Musical'}

award_mapping_pres = {'Best Score award': 'Best Original Score',
	'Best Actress Comedy or Musical': 'Best Actress in a Motion Picture - Comedy or Musical',
	'Best Actress in a Motion Picture, Drama': 'Best Actress in a Motion Picture - Drama',
	'best animated film': 'Best Animated Feature Film',
	'best TV series comedy or musical': 'Best Television Series - Comedy or Musical',
	'Best Actress in a TV Comedy': 'Best TV Series Actress - Comedy or Musical',
	'Best Screenplay - Motion Picture': 'Best Screenplay',
	'best supporting actress in a series, mini-series or tv movie': 'Best Supporting Actress in a TV Movie, Series, or Miniseries',
	'Cecil B. DeMille lifetime achievement award': 'Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures',
	'presenting Best Director': 'Best Director',
	'Best Motion Picture Comedy or Musical': 'Best Motion Picture - Comedy or Musical',
	'Best Actress in a TV Series - Drama': 'Best Actress in a Television Series - Drama',
	'Best Supporting Actor in a Motion Picture': 'Best Supporting Actor in a Motion Picture',
	'presents Best Motion Picture, Drama': 'Best Motion Picture - Drama',
	'announced Best TV Drama': 'Best Television Series - Drama',
	'best foreign film': 'Best Foreign Film',
	'presetan al MEJOR ACTOR EN UNA SERIE DE TV MINISERIE O PELI PARA TV': 'Best Supporting Actor in a Television Series',
	'she has to stand on stage with': 'Best Actor in a Television Series - Comedy or Musical',
	'are the first presenters': 'Best Supporting Actress in a Motion Picture',
	'que tem um chiclete na boca': 'Best Actor in a TV Movie or Miniseries',
	'presentan el premio a Mejor Miniserie': 'Best Miniseries or Motion Picture Made for Television',
	'Nadie se le acerca': 'Best Actor in a Motion Picture - Comedy or Musical',
	'present the Best Score award': 'Best Original Song',
	'presentando el premio a Mejor Actor en una pelicula dramatica': 'Best Actor in a Motion Picture - Drama',
	'Mejor Actor de Serie Dram': 'Best Television Series Actor - Drama',
	}
	
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

def get_dict_buckets(filename):
	text_file = open(filename, "r")
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
	names.append('Halle')
	names.append('Salma')
	sentences = sent_detector.tokenize(text)
	entities = []
	stoplist = ["Justin REALLY", "Clinton Endorses"]
	for sentence in sentences:
		temp = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))
		i = 0
		for entity in temp:
			i +=1
			try:
				nodeLabel = entity.node;
			except AttributeError:
				pass
			else:
				if (len(entity)==2 and entity[0][0] in names):
					person = entity[0][0]+" "+entity[1][0]
					if (person in stoplist):
						pass
					else:
						entities.append(person)
				elif (nodeLabel=='PERSON' and len(entity)==1 and entity[0][0] in names):
					try:
						nextNodeLabel = temp[i].node
					except AttributeError:
						pass
					except IndexError:
						pass
					else:
						person = entity[0][0]+" "+temp[i][0][0]
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
						winner = temp_array[1]
					if length == 4:
						#[award, category, winer, movie ]
						print temp_array[0]+ "- " +temp_array[1]+ "- "+temp_array[2] +"- "+temp_array[3]
						winner = temp_array[2]
					if length == 2:
						#[award, winner]
						print temp_array[0] + "- "+temp_array[1]
						winner = temp_array[1]
					for winner in temp_array[1::]:
						if winner not in winners_lower:
							winners_lower.append(winner.lower().replace(" ",""))
		if "Cecil" in tweet_text:
			cecil_award.append(tweet_text)
	cecil_winner = find_most_popular(cecil_award[:30])[0]
	print "Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures - " + cecil_winner
	winners_lower.append(cecil_winner.lower().replace(" ",""))
	print ""


#makes a dictionary with buckets dictated in filename
def make_tweet_dict(filename):
	dict_buckets = get_dict_buckets(filename)
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

def find_hosts():
	print "--HOSTS--"
	host_tweet_dict = make_tweet_dict("dict_hosts.txt")
	hosts = find_most_popular(host_tweet_dict['hosted'][0:50])
	host0 = hosts[0]
	host1 = hosts[1]
	hosts_lower.append(host0.lower().replace(" ",""))
	hosts_lower.append(host1.lower().replace(" ",""))
	print tweet_dict
	print host0 + " and " + host1


#TODO: make this faster.
def find_most_popular(tweet_pool, stoplist = []):
	name_array = numpy.array([])
	count_array = numpy.array([])
	for tweet in tweet_pool:
		people = person_search(tweet)
		if len(people):
			for person in people:
				if person.lower().replace(" ","") not in stoplist:
					if person in name_array:
						index = numpy.where(name_array==person)[0][0]
						count_array[index] += 1
					else:
						name_array = numpy.append(name_array,person)
						count_array = numpy.append(count_array,1)
	sorting = count_array.argsort()
	sorting = sorting[::-1]
	sorted_name_array = name_array[sorting]

	return sorted_name_array

def find_nominees():
	tweet_dict = make_tweet_dict("dict_nominees.txt")
	awards = get_dict_buckets("dict_nominees.txt")
	people={}
	stoplist = winners_lower + hosts_lower + presenters_lower + random_lower
	for award in awards:
		people[award] = find_most_popular(tweet_dict[award], stoplist)
	print "--NOMINEES--"
	for award in people.keys():
		p = people[award]
		print "For " + award_mapping[award] + ": ",
		lim = 0
		for p1 in p:
			lim = lim +1
			print p1 + " ",
			if lim == 3:
				break
		print ""
	return

def find_presenters():
	tweet_dict = make_tweet_dict("dict_presenters.txt")
	awards = get_dict_buckets("dict_presenters.txt")
	presenters = {}
	stop_list = winners_lower + hosts_lower
	stop_list.append('alberteinstein')
	stop_list.append('carriemathison')
	stop_list.append('lovechristoph')
	print "--PRESENTERS--"
	for award in awards:
		presenters[award] = find_most_popular(tweet_dict[award], stop_list)
	for award in presenters.keys():
		pres_string = award_mapping_pres[award] + ": "
		for person in presenters[award]:
			if person.lower().replace(" ","") not in stop_list:
				pres_string+=person + " "
				sentiment_output(sentimental_tweets(person))
		print pres_string
	return

def sentimental_tweets(string):
	sent_dict = {'positive': [], 'negative': []}
	list = find_tweets(string)
	for tweet in list:
		sentiment = feelings.classify_tweet(tweet)
		sent_dict[sentiment].append(tweet)
	return sent_dict

def sentiment_output(dict):
	ratio = float(len(dict['positive']))/(float(len(dict['negative']))+float(len(dict['positive'])))
	ratio = round(ratio*100)
	if (ratio > 50):
		print str(ratio) + "% Positive" + dict['positive'][0]
	else:
		print str(ratio) + "% Positive: " + dict['negative'][0]
	return

def find_presenter_list():
	presenters = []
	not_winners = []
	for tweet in tweets:
		if "presenting" in tweet["text"].lower():
			presenters.append(tweet["text"])
	#print "--PRESENTERS--"
	people = find_most_popular(presenters)
	for person in people:
		if person.lower().replace(" ","") not in  winners: 
			not_winners.append(person)

	return not_winners

def print_tweets(string):
	for tweet in tweets:
		if string in tweet['text']:
			print tweet['text']
	return


def main():
	find_hosts()
	find_winners()
	find_presenters()
	find_nominees()

# main()