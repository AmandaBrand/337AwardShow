import re
import csv
import pprint
import nltk
import nltk.classify


# clean up the tweets
def cleanup(tweet):
    # lower case
    tweet = tweet.lower()
    # URLs
    tweet = re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet)
    # usernames
    tweet = re.sub('@[^\s]+', 'USERNAME', tweet)
    # white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # hastags
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet


# remove repeats
def repeat(x):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return pattern.sub(r"\1\1", x)


# get stopwords
def stopWords(filename):
    swlist = []
    f = open(filename, 'r')
    line = f.readline()
    while line:
        word = line.strip()
        swlist.append(word)
        line = f.readline()
    f.close()
    return swlist


def getFeatures(tweet, sw):
    featureVector = []  
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences 
        w = repeat(w) 
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if it consists of only words
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        #ignore if it is a stopWord
        if (w in sw or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector    


def extractFeatures(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in tweet_words)
    #print features
    return features


#==================================================
#==================================================
#==================================================


"""
create a single list of tweets by reading in the tweets.csv file
cleaning up the tweets, filtering words and removing stopwords, 
and tagging each set of words from the tweets with their sentiment (tuples)
"""

tweetlist = csv.reader(open('tweets.csv', 'rb'), delimiter=',', quotechar='|')
stoppers = stopWords('stopwords.txt')
word_features = []
tweets = []

for row in tweetlist:
    sentiment = row[0]
    tweet = row[1]
    cleantweet = cleanup(tweet)
    words_filtered = [e.lower() for e in tweet.split() if len(e) >= 3]
    words = getFeatures(cleantweet, stoppers)
    word_features.extend(words)
    tweets.append((words_filtered , sentiment))
    #print words



"""
apply features to classifier to train it. using NLTK and NaiveBayesClassifier
"""


training_set = nltk.classify.util.apply_features(extractFeatures, tweets)

classifier = nltk.NaiveBayesClassifier.train(training_set)
"""
now we can test the sentiment analysis
"""


def classify_tweet(tweet):
    sentiment = classifier.classify(extractFeatures(cleanup(tweet).split()))
    return sentiment



# test = 'My soul died just a little'

# print "Test Tweet = %s\n" % (test)
# print "Sentiment = %s\n" % (sentiment)

# test2 = 'I\'m at a loss for words'
# sentiment = classifier.classify(extractFeatures(test2.split()))
# print "Test Tweet = %s\n" % (test2)
# print "Sentiment = %s\n" % (sentiment)
