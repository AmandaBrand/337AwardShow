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


# On The Red Carpet 
print "--FASHION ON THE RED CARPET--"

with open('goldenglobes.json', 'r') as f:
     tweets = map(json.loads, f)

#tweet_dict = make_tweet_dict("dict_dressed.txt")
redcarpet = open('redcarpet.txt', 'w')
celebs = []

for tweet in tweets:
	tweet_text = tweet['text']
	ctweet = clean(tweet_text).encode('utf-8')
	if "wearing" in ctweet:
		#celebs.append(person_search(ctweet))
#print celebs		
  		redcarpet.write("%s\n" % ctweet)

# to find the designer
#print "CELEBS:"
#
#for i in celebs:





# tweet2 = 'And John Cena presents the award for Best Actress'
# print classify(tweet2)
#print classifier.show_most_informative_features(200)
#print nltk.classify.accuracy(classifier, tweet2)

# print informative features about the classifier
# print classifier.show_most_informative_features(10)
