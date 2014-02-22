import re, csv, pprint, nltk, nltk.classify, svm
from svmutil import * 


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
    #print featureVector
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
pos_f = csv.reader(open('pos_features.csv', 'rU'), delimiter=',', quotechar='|')
neg_f = csv.reader(open('neg_features.csv', 'rU'), delimiter=',', quotechar='|')
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
    #print tweets

# add in other features to help train the classifier
for i in pos_f and neg_f:
    sentiment = i[0]
    feat = i[1]
    tweets.append(([feat], sentiment))
    #print tweets

#print tweets
"""
apply features to classifier to train it. using NLTK and NaiveBayesClassifier
"""


training_set = nltk.classify.util.apply_features(extractFeatures, tweets)


"""
now we can test the sentinment analysis - using Support Vector Machines
"""


# classifier = nltk.NaiveBayesClassifier.train(training_set)

# def classify(tweet):
#     sentiment = classifier.classify(extractFeatures(cleanup(tweet).split()))
#     return sentiment



# test = 'My soul died just a little'

# print "Test Tweet = %s\n" % (test)
# print "Sentiment = %s\n" % (sentiment)

# test2 = 'I\'m at a loss for words'
# sentiment = classifier.classify(extractFeatures(test2.split()))
# print "Test Tweet = %s\n" % (test2)
# print "Sentiment = %s\n" % (sentiment)

def getSVMFeatureVectorAndLabels(tweets, featureList):
    sortedFeatures = sorted(featureList)
    map = {}
    feature_vector = []
    labels = []
    for t in tweets:
        label = 0
        map = {}
        #Initialize empty map
        for w in sortedFeatures:
            map[w] = 0
        
        tweet_words = t[0]
        tweet_opinion = t[1]
        #Fill the map
        for word in tweet_words:
            #process the word (remove repetitions and punctuations)
            word = replaceTwoOrMore(word) 
            word = word.strip('\'"?,.')
            #set map[word] to 1 if word exists
            if word in map:
                map[word] = 1
        #end for loop
        values = map.values()
        feature_vector.append(values)
        if(tweet_opinion == 'positive'):
            label = 0
        elif(tweet_opinion == 'negative'):
            label = 1
        elif(tweet_opinion == 'neutral'):
            label = 2
        labels.append(label)            
    #return the list of feature_vector and labels
    return {'feature_vector' : feature_vector, 'labels': labels}
#end
 
#Train the classifier
result = getSVMFeatureVectorandLabels(tweets, featureList)
problem = svm_problem(result['labels'], result['feature_vector'])
#'-q' option suppress console output
param = svm_parameter('-q')
param.kernel_type = LINEAR
classifier = svm_train(problem, param)
svm_save_model(classifierDumpFile, classifier)
 
#Test the classifier
test_feature_vector = getSVMFeatureVector(test_tweets, featureList)
#p_labels contains the final labeling result
p_labels, p_accs, p_vals = svm_predict([0] * len(test_feature_vector),test_feature_vector, classifier)
