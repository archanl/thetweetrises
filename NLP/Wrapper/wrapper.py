import Queue
import threading
import urllib2
from sklearn import linear_model
from nltk.classify import SklearnClassifier
from sklearn.svm import SVC
from nltk.classify import MaxentClassifier
import heapq
import math
import numpy as np
import re
import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../NaiveBayes')
sys.path.insert(0, '../StochasticGradientDescent')
sys.path.insert(0, '../SupportVectorMachine')
sys.path.insert(0, '../MaximumEntropy')
from definitions import *
import cPickle


DEBUG = True


class classifier_wrapper:
	def __init__(self):
	    t1 = threading.Thread(target=self.train_naive_bayes)
	    t1.daemon = True
	    t1.start()
	    t2 = threading.Thread(target=self.train_sgd)
	    t2.daemon = True
	    t2.start()
	    t3 = threading.Thread(target=self.train_support_vector_machine)
	    t3.daemon = True
	    t3.start()
	    t4 = threading.Thread(target=self.train_maximum_entropy)
	    t4.daemon = True
	    t4.start()
	    t1.join()
	    t2.join()
	    t3.join()
	    t4.join()

	def train_all(self):
		self.train_naive_bayes();
		self.train_sgd();
		self.train_support_vector_machine();
		self.train_maximum_entropy();

	def train_naive_bayes(self):
		new_naive_bayes_classifier(self);

	def train_sgd(self):
		new_sgd_classifier(self);

	def train_support_vector_machine(self):
		new_svm_classifier(self);

	def train_maximum_entropy(self):
		new_maximum_entropy_classifier(self);

	def classify(self, tweet, algorithm):
		if algorithm == "sgd":
			bag = get_words(tweet, self.stop_words)

			# Get classification
			point = get_sgd_point(bag, self.top_sgd_terms)
			cls = self.sgd_classifier.classify(point)

		elif algorithm == "naive_bayes":
			bag = get_words(tweet, self.stop_words)

			# Get classification
			cls = get_classification(bag, self.top_naive_bayes_terms, self.naive_bayes_positive_classifications, self.naive_bayes_negative_classifications, self.naive_bayes_terms)

		elif algorithm == "svm":
			bag = get_words(tweet, self.stop_words)
			
			fv = {}
			for word in bag:
				if word in self.top_svm_terms:
					fv[word] = 1

			# Get classification
			pdist = self.svm_classifier.prob_classify(fv)
            if pdist.prob(0) > tolerance:
                cls = 0
            elif pdist.prob(4) > tolerance:
                cls = 4
            else:
                cls = 2

		elif algorithm == "maximum_entropy":
			bag = get_words(tweet, self.stop_words)
			
			fv = {}
			for word in bag:
				if word in self.top_maxent_terms:
					fv[word] = 1

			# Get classification
			#point = get_point(bag, self.top_maxent_terms)
			pdist = self.maxent_classifier.classify(fv)
            if pdist.prob(0) > tolerance:
                cls = 0
            elif pdistprob(4) > tolerance:
                cls = 4
            else:
                cls = 2

		else:
			raise Exception("Invalid algorithm choice: " + algorithm)

		if cls == 4.0:
			return "positive"
		return "negative"









def new_sgd_classifier(wrapper):
	c_sgd, top_terms, stop_words = get_svm_classifier();
	wrapper.sgd_classifier = c_sgd
	wrapper.top_sgd_terms = top_terms
	wrapper.stop_words = stop_words


def new_naive_bayes_classifier(wrapper):
	top_terms, pos_classifications, neg_classifications, stop_words, naive_bayes_terms = get_naive_bayes_classifier();
	wrapper.top_naive_bayes_terms = top_terms;
	wrapper.naive_bayes_positive_classifications = pos_classifications;
	wrapper.naive_bayes_negative_classifications = neg_classifications;
	wrapper.stop_words = stop_words;
	wrapper.naive_bayes_terms = naive_bayes_terms;


def new_maximum_entropy_classifier(wrapper):
	m_classifier, stop_words, top_terms = get_maxent_classifier();
	wrapper.maxent_classifier = m_classifier;
	wrapper.stop_words = stop_words;
	wrapper.top_maxent_terms = top_terms;


def new_svm_classifier(wrapper):
	c_svm, top_terms, stop_words = get_svm_classifier();
	wrapper.svm_classifier = c_svm;
	wrapper.top_svm_terms = top_terms;
	wrapper.stop_words = stop_words;

















def get_classification(bag, top_terms, positive_classifications, negative_classifications, terms):
	''' Uses Naive bayes to classify the bag of words (a tweet) using the
		terms in the list 'top_terms' and the training data "go_tweets"'''

	prob_neg = 1
	prob_pos = 1

	for word in top_terms:
		prob_word_in_pos = float(terms[word].positive) / positive_classifications
		prob_word_in_neg = float(terms[word].negative) / negative_classifications

		if word in bag:
			prob_neg = prob_neg * prob_word_in_neg
			prob_pos = prob_pos * prob_word_in_pos
		else:
			prob_neg = prob_neg * (1 - prob_word_in_neg)
			prob_pos = prob_pos * (1 - prob_word_in_pos)

	# Debug
	#print "prob_neg: %f" % prob_neg
	#print "prob_pos: %f" % prob_pos

	if prob_neg > prob_pos:
		return 0
	return 4





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

def get_sgd_point(bag, terms):
	''' Make a point from the `bag` which represents a sentence '''
	fv = {}
	for word in bag:
		if word in terms:
			fv[word] = 1
	# sk-learn must have a list of points
	return fv







def get_sgd_classifier():

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
	term_limit = 600

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

	return clf, top_terms, stop_words







def get_svm_classifier():

	print "Loading training data..."

	#test = np.zeros((100000, 10000))

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
	upto = 10000
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
	term_limit = 5000

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

	#TODO
	# Train
	num_features = len(top_terms)
	num_samples = len(go_tweets)
	#X = np.zeros((num_samples, num_features))
	train = []
	#y = []
	for (score, bag) in go_tweets:
		fv = {}
			# feature vector for this tweet
		for word in bag:
			if word in top_terms:
				fv[word] = 1
				
		train.append( (fv, score) )
	#Y = np.array(y)


	'''print (X)
	print (Y)
	assert False'''

	print "Fitting data..."
	classifier = SklearnClassifier(SVC(kernel='linear', probability=True)).train(train)

	return classifier, top_terms, stop_words






def get_naive_bayes_classifier():
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
	upto = 1000000
	do_debug_limit = False 

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

	# Debug
	print "Total number of terms: %d" % len(terms)
	#assert False

	# Get the top number of terms
	print "Getting top terms from mutual information"
	scores = []
	top_terms = []
	term_limit = 5000

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

	print "Top terms found"


	return top_terms, positive_classifications, negative_classifications, stop_words, terms










def get_maxent_classifier():

	print "Loading training data..."

	#test = np.zeros((100000, 10000))

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
	upto = 10000
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
	term_limit = 1000

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

	#TODO
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
	#clf = linear_model.SGDClassifier()
	# Default linear_model.SGDClassifier settings:
	#SGDClassifier(alpha=0.0001, class_weight=None, epsilon=0.1, eta0=0.0,
	#        fit_intercept=True, l1_ratio=0.15, learning_rate='optimal',
	#        loss='hinge', n_iter=5, n_jobs=1, penalty='l2', power_t=0.5,
	#        random_state=None, rho=None, shuffle=False,
	#        verbose=0, warm_start=False)
	#print "Fitting data..."
	#clf.fit(X, Y)
	#print "Data fitted!"
	# Example prediction
	#print(clf.predict([[-0.8, -1]]))

	return classifier, stop_words, top_terms;










if __name__ == "__main__":
	thewrapper = classifier_wrapper(); 
	f = open("test.txt", 'wb')
	cPickle.dump(thewrapper, f)
	f.close()
