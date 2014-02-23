import re, json, csv, pprint, nltk
from feelings import *

tweet2 = 'I didn\'t like his speech'
print tweet2
print classify_tweet(tweet2)
print classifier.show_most_informative_features(200)