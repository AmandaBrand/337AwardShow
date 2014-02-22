import pprint, re, csv, nltk, nltk.classify


def cleanup(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r'http\:\/\/t\.co\/.+', "", tweet)
    tweet = re.sub(r'\(@.+\)', 'USERNAME', tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = tweet.strip('\'"')
    return tweet


def repeat(x):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return pattern.sub(r"\1\1", x)


def stopWords():
    swlist = []
    f = open('stopwords.txt', 'r')
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
        w = repeat(w) 
        w = w.strip('\'"?,.')
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
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
    return features



"""
create a single list of tweets by reading in the tweets.csv file
cleaning up the tweets, filtering words and removing stopwords, 
and tagging each set of words from the tweets with their sentiment (tuples)
"""

tweetlist = csv.reader(open('tweets.csv', 'rb'), delimiter=',', quotechar='|')
pos_f = csv.reader(open('pos_features.csv', 'rU'), delimiter=',', quotechar='|')
neg_f = csv.reader(open('neg_features.csv', 'rU'), delimiter=',', quotechar='|')
stoppers = stopWords()
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

# add in other features to help train the classifier
for i in pos_f and neg_f:
    sentiment = i[0]
    feat = i[1]
    tweets.append(([feat], sentiment))


"""
apply features to classifier to train it. using NLTK and NaiveBayesClassifier
"""


training_set = nltk.classify.util.apply_features(extractFeatures, tweets)

classifier = nltk.NaiveBayesClassifier.train(training_set)


"""
test the sentiment analyzer
"""


classifier = nltk.NaiveBayesClassifier.train(training_set)

def classify_tweet(tweet):
    sentiment = classifier.classify(extractFeatures(cleanup(tweet).split()))
    return sentiment



# test = 'My soul died just a little'
# sentiment = classifier.classify(extractFeatures(cleanup(test).split()))
# print "Test Tweet = %s\n" % (test)
# print "Sentiment = %s\n" % (sentiment)

# test2 = 'I\'m at a loss for words'
# sentiment = classifier.classify(extractFeatures(cleanup(test2).split()))
# print "Test Tweet = %s\n" % (test2)
# print "Sentiment = %s\n" % (sentiment)
