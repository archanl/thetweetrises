from sklearn import linear_model
from nltk.classify import SklearnClassifier
import heapq
import math
import numpy as np
import re
import sys
sys.path.insert(0, '..')
from definitions import *




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

def get_point(bag, terms):
	''' Make a point from the `bag` which represents a sentence '''
	fv = {}
	for word in bag:
		if word in terms:
			fv[word] = 1
	# sk-learn must have a list of points
	return fv



def get_classifier():
	

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
	upto = 100000
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
	term_limit = 600
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



	print top_terms.keys()[0:100]



	# Debug
	print "Total number of features: %d" % len(top_terms)
	#assert False

	# Train
	num_features = len(top_terms)
	num_samples = len(go_tweets)
	y = []
	train = []
	for (score, bag) in go_tweets:
		y.append(score)
		fv = {}
			# feature vector for this tweet
		for word in bag:
			if word in top_terms:
				fv[word] = 1
				
		train.append( (fv, score) )
	Y = np.array(y)

	
	print "Fitting data..."
	clf = SklearnClassifier(linear_model.SGDClassifier(n_iter = 40, fit_intercept = False, alpha = 0.001, l1_ratio = 0.30), sparse=False).train(train)
	#clf = linear_model.SGDClassifier()
	#clf.fit()
	print "Data fitted!"

	return clf



if __name__ == "__main__":

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
	upto = 100000
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
	term_limit = 600
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



	print top_terms.keys()[0:100]



	# Debug
	print "Total number of features: %d" % len(top_terms)
	#assert False

	# Train
	num_features = len(top_terms)
	num_samples = len(go_tweets)
	y = []
	train = []
	for (score, bag) in go_tweets:
		y.append(score)
		fv = {}
			# feature vector for this tweet
		for word in bag:
			if word in top_terms:
				fv[word] = 1
				
		train.append( (fv, score) )
	Y = np.array(y)

	





	
	print "Fitting data..."
	clf = SklearnClassifier(linear_model.SGDClassifier(n_iter = 40, fit_intercept = False, alpha = 0.001, l1_ratio = 0.30), sparse=False).train(train)
	#clf = linear_model.SGDClassifier()
	#clf.fit()
	print "Data fitted!"

	# Loop through test data
	
	print "Running on test data..."

	go_test_data = open(GO_TEST_DATA)
	correct_classifications = 0;
	total_classifications = 0;
	pos_classifications = 0
	neg_classifications = 0
	
	for line in go_test_data:
		parts = line.split(",")
		score = float(parts[0].replace('"', ""))
		if score == 0 or score == 4:
			bag = get_words(parts[5], stop_words)

			# Get classification
			point = get_point(bag, top_terms)
			cls = clf.classify(point)

			if cls == 4.0:
				pos_classifications = pos_classifications + 1
			else:
				neg_classifications = neg_classifications + 1



			# Compare to the correct classification
			if cls == score:
				correct_classifications = correct_classifications + 1

			total_classifications = total_classifications + 1

	print "Positive classifications: " + str(pos_classifications)
	print "Negative classifications: " + str(neg_classifications)
	print "The percentage correct was: %g" % (float(correct_classifications) / float(total_classifications))