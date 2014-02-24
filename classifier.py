import re, json, csv, pprint, nltk, awardshow
from feelings import *
from awardshow import *

"""
1. extract the tweets that deal with what the celebrities are wearing
2. find a way to extract the names of the celebrities
3. figure out a way to extract the name of the designer
4. use sentiment analysis to display how people felt about the
	what the celebrity was wearing, also print a sample
"""

with open('goldenglobes.json', 'r') as f:
     tweets = map(json.loads, f)


# On The Red Carpet 
print "--FASHION ON THE RED CARPET--"


redcarpet = open('redcarpet.txt', 'r+')
categorized = []
celebs = []
fashion = {}
designers = ['Alexander McQueen', 'Tom Ford', 'Atelier Versace', 
			 'L\'Wren Scott', 'J Mendel', 'Laura Mercier', 'Harry Winston',
			 'Zuhair Murad', 'Charlotte Olympia', 'Roberto Cavalli',
			 'Ellie Saab', 'Naeem Khan', 'Hugo Boss', 'Vera Wang',
			 'Bob Mackie', 'Jenny Packam', 'Bonnie Belle', 'Ralph Lauren',
			 'Scott Golden']
clothes = ['dress', 'gown', 'tie', 'shoes', 'necklace', 'jewelry', 'belt']
others = []
stop = ['Dennis Quad', 'Tom Ford', 'Red Carpet', 'Jen Lawrence', 'Kristin Wiig',
		'Sofia Veraga', 'Red Carpets', 'Taylor Swifts', 'Kristen Wig', 'Lucy Lu',
		'Kristin Bell', 'Red Wings', 'Elie Saab']
# info = []

for tweet in tweets:
	tweet_text = tweet['text']
	ctweet = clean(tweet_text).encode('utf-8')
	# words = tweet_text.split()
	# for w in words:	
	# 	if w in stoppers:
	# 		continue
	# 	else:
	# 		info.append(w.lower())
	# print words

	if "wearing" in ctweet:
		#redcarpet.write("%s\n" % ctweet)
		celebs.append(person_search(ctweet))	
	

# analyze people's sentiments over what they're wearing
def sentimental_tweets(string):
	sent_dict = {'positive': [], 'negative': []}
	pos = 0
	neg = 0

	for tweet in redcarpet:
		if str(string) in tweet:
			sentiment = feelings.classify_tweet(clean(tweet))
			if sentiment == 'positive':
				pos += 1
			elif sentiment == 'negative':
				neg += 1
		else:
			continue

	denom = pos + neg
	if denom != 0:
		pos_ratio = round((pos/(pos+neg))*100)
		neg_ratio = round((neg/(pos+neg))*100)

		print str(pos_ratio) + "% said Fab "
		print str(neg_ratio) + "% said Drab "
	return


# find "wearing" and get everything after that
for i in celebs:
	if i not in categorized:
		if len(i) == 0:
			# if "is wearing" in j:
			# 	start = j.find('is wearing')
			# 	end = j.find(' at', start)
			# 	dress = j[start:end]
			# 	name = person_search(j)
			# 	categorized.append(name)
			# 	print name, dress
			# else: 
			continue
		
		elif len(i) == 1:
			name = i[0]
			others.append(name)
			# print name
			# sentiment = sentimental_tweets(name.lower())
			categorized.append(i)
		
		elif len(i) == 2: 
			name = i[0]
			designer = i[1]
			categorized.append(i)
			categorized.append(name)
			if designer in designers:
				real = 'L\'Wren Scott'
				if designer == 'Scott Golden': designer = real
				print name + ' was wearing a piece by designer ' + designer + ' on the Red Carpet.'
				sentimental_tweets(name.lower())
			else:
				others.append(name)
				# print name
				# sentiment = sentiment_output(sentimental_tweets(name.lower()))		
				continue

print '\n'
print "Other Celebrities: "
for i in others:
	if i not in categorized:
		if i not in stop:
			print i
			sentimental_tweets(i.lower())
			categorized.append(i)
			print '\n'
	else:
		continue
