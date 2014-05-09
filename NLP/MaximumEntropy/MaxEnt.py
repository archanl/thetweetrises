import heapq
import math
import numpy as np
from nltk.classify import MaxentClassifier
import re
import sys
sys.path.insert(0, '..')
from definitions import *
sys.path.insert(0, '../Wrapper/')
from helper import *

def get_maxent_classifier():
    print "Loading training data..."

    # A dictionary whose keys are strings (words) and values are tweetclass objects
    terms = {}

    # Load training data
    go_training_data = open(GO_TRAINING_DATA)
    go_tweets = []

    # Load stop words
    sw = open(STOP_WORDS_DATA)
    stop_words = {}
    for line in sw:
        stop_words[line.strip()] = True
    
    # DEBUG
    debug_counter = 0
    positive_counter = 0
    negative_counter = 0
    # A debug limit for the number of positive and negative tweets
    upto = MAXIMUM_ENTROPY_TWEET_LIMIT
    do_debug_limit = True 

    if DEBUG:
        upto = 1000
        do_debug_limit = True

    for line in go_training_data:
        # Parse the line for the classification and the tweet
        parts = line.split(",")
        score = float(parts[0].replace('"', ""))
        # Debug
        if do_debug_limit:
            if score == 0:
                if negative_counter >= upto:
                    continue
                negative_counter = negative_counter + 1
            else:
                if positive_counter >= upto:
                    continue
                positive_counter = positive_counter + 1
        
        bag = get_words(parts[5], stop_words)
        go_tweets.append((score, bag))
    
        # Add all the words in the tweet to the list of all terms
        for word in bag:
            if word not in terms:
                nt = tweetclass(word)
                if score == 0:
                    nt.negative = 1
                    nt.positive = 0
                else:
                    nt.positive = 1
                    nt.negative = 0
                terms[word] = nt
            else:
                if score == 0:
                    terms[word].negative = terms[word].negative + 1
                else:
                    terms[word].positive = terms[word].positive + 1

        # Debug
        debug_counter = debug_counter + 1
        if debug_counter % 1000 == 0:
            print "processed %d tweets" % debug_counter
            

    negative_classifications = 0
    for (score, bag) in go_tweets:
        if score == 0:
            negative_classifications = negative_classifications + 1
    positive_classifications = len(go_tweets) - negative_classifications

    print "Training data loaded!"


    
    # Get the top number of terms
    print "Getting top terms from mutual information"
    scores = []
    top_terms = []
    term_limit = MAXIMUM_ENTROPY_TERM_LIMIT

    if DEBUG:
        term_limit = 50

    heap_terms_processed = 0
    for term in terms:
        score = get_score(term, positive_classifications, negative_classifications, terms)
        # Debug
        #print "score: %f\tterm: %s" % (score, term)
        if heap_terms_processed % 1000 == 0:
            print "heap terms processed: %d" % heap_terms_processed
        heapq.heappush(scores, (score, term))
        if len(scores) > term_limit:
            heapq.heappop(scores)
        assert len(scores) <= term_limit
        heap_terms_processed = heap_terms_processed + 1

    for item in scores:
        top_terms.append(item[1])

    tt = top_terms
    top_terms = {}
    for t in tt:
        top_terms[t] = True


    print "Top terms found"





    # Debug
    print "Total number of terms: %d" % len(terms)
    #assert False

    # Train
    num_features = len(top_terms)
    num_samples = len(go_tweets)
    train = []
    for (score, bag) in go_tweets:
        fv = {}
            # feature vector for this tweet
        for word in bag:
            if word in top_terms:
                fv[word] = 1
                
        train.append( (fv, score) )


    print "Fitting data..."
    classifier = MaxentClassifier.train(train, algorithm='IIs', trace=0, max_iter=100)
    print "Data fitted!"

    return classifier, stop_words, top_terms;

