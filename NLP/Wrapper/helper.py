import re
import math

class parameters:
    def __init__(self, upto, term_limit, alpha, l1_ratio, kernel, iterations):
        self.upto = upto
	self.term_limit = term_limit
	self.alpha = alpha
	self.l1_ratio = l1_ratio
	self.kernel = kernel
	self.iterations = iterations

class tweetclass:
    def __init__(self, word):
        self.term = word
        self.positive = 0
        self.negative = 0

def twocharreplacement(tweet):
    nt = ""
    for i in range(len(tweet)):
        if i >= 2:
            if not (tweet[i - 2] == tweet[i - 1] == tweet[i]):
                nt += tweet[i]
        else:
            nt += tweet[i]
        i += 1
    return nt

def get_words(tweet, stop_words):
    ''' Parses all of the words from a tweet '''
    tweet = tweet.lower()

    # replace characters that occur twice in a row
    tweet = twocharreplacement(tweet)
    
    # Find n-grams
    unigrams = re.findall("[a-zA-Z][a-zA-Z]+", tweet)
    #twograms = re.findall("(?=((?:\s|^)[a-zA-Z] [a-zA-Z]+))", tweet)
    #threegrams = re.findall("(?=((?:\s|^)[a-zA-Z] [a-zA-Z] [a-zA-Z]+))", tweet)
    
    allwords = unigrams

    bag = {}
    for word in allwords:
        if word not in stop_words:
            bag[word.strip()] = True

    if tweet.find('?') != -1:
        bag['?'] = True
    if tweet.find('!') != -1:
        bag['!'] = True
    if tweet.find('.') != -1:
        bag['.'] = True

    return bag

def get_score(term, positive_classifications, negative_classifications, terms):
    ''' Gets the Mutual Information score of a term based on the training data'''
    # Term in tweet and classifier is positive
    n_11 = terms[term].positive
    # Term in tweet and classifier is negative
    n_10 = terms[term].negative
    # Term not in tweet and classfier is positive
    n_01 = positive_classifications - n_11
    # Term not in tweet and classfier is negative
    n_00 = negative_classifications - n_10
    


    # Total number of tweets
    N = n_11 + n_10 + n_01 + n_00

    N_1 = n_11 + n_10
    N_2 = n_11 + n_01
    N_3 = n_10 + n_00
    N_4 = n_01 + n_00

    # Debug
    #print "n_11: %d, n_10: %d, n_01: %d, n_00: %d" % (n_11, n_10, n_01, n_00)
    #print "N_1: %d, N_2: %d, N_3: %d, N_4: %d" % (N_1, N_2, N_3, N_4)
    
    score = 0
    if n_11 != 0:
        score = score + float(n_11) / float(N) * math.log(float(n_11 * N) / float(N_1 * N_2), 2)
    if n_01 != 0:
        score = score + float(n_01) / float(N) * math.log(float(n_01 * N) / float(N_4 * N_2), 2)
    if n_10 != 0:
        score = score + float(n_10) / float(N) * math.log(float(n_10 * N) / float(N_1 * N_3), 2)
    if n_00 != 0:
        score = score + float(n_00) / float(N) * math.log(float(n_00 * N) / float(N_4 * N_3), 2)

    return score

