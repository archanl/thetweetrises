import Queue
import threading
import urllib2
from sklearn import linear_model
from nltk.classify import SklearnClassifier
from sklearn.svm import SVC
from nltk.classify import MaxentClassifier
import heapq
import numpy as np
import sys
from helper import *
sys.path.insert(0, '../')
from definitions import *
sys.path.insert(0, '../NaiveBayes')
from NaiveBayes import *
sys.path.insert(0, '../StochasticGradientDescent')
from SGD import *
sys.path.insert(0, '../SupportVectorMachine')
from SVM import *
sys.path.insert(0, '../MaximumEntropy')
from MaxEnt import *
import cPickle
from time import time

class classifier_wrapper:
    def __init__(self):
    	return

    def do_training(self):
	upto = 10000
	the_parameter = parameters(upto, 1000, .001, .3, 'linear', 100)
	self.train_support_vector_machine(the_parameter)
	self.train_maximum_entropy(the_parameter)
	self.train_sgd(the_parameter)
	the_parameter.upto = 100000
	self.train_naive_bayes(the_parameter)

    def make_graphs(self):
	# Get 1000 tweets from the test set
	tweets = self.get_test_tweets(1000)

	'''
	the_parameter = parameters(20 * 200, 1000, .001, .3, 'linear', 100)
	self.train_naive_bayes(the_parameter)
	tt = self.get_test_tweets(3000)
	results = self.test_classification(tt)
	print results
	return
	'''

	'''
	print "starting accuracy tests..."

	file1 = open(PLOT_TIME_MAXENT_FILE, 'w')
	file2 = open(PLOT_TIME_NAIVE_BAYES_FILE, 'w')
	file3 = open(PLOT_TIME_SGD_FILE, 'w')
	file4 = open(PLOT_TIME_SVM_FILE, 'w')
	#for i in range(1, 2):
	for i in range(2, 21, 2):
		upto = i * 500
		the_parameter = parameters(upto, 1000, .001, .3, 'linear', 100)
		#the_parameter = parameters(10000, 1000, .001, .3, 'linear', 100)
		support_time = time()
		self.train_support_vector_machine(the_parameter)
		support_time = time() - support_time
		naive_bayes_time = time()
		self.train_naive_bayes(the_parameter)
		naive_bayes_time = time() - naive_bayes_time
		max_ent_time = time()
		self.train_maximum_entropy(the_parameter)
		max_ent_time = time() - max_ent_time
		sgd_time=  time()
		self.train_sgd(the_parameter)
		sgd_time = time() - sgd_time
		# Do classification with the tweets and get the % accuracy
		results = self.do_all_classification(tweets)
		results["support_time"] = support_time
		results["max_ent_time"] = max_ent_time
		results["sgd_time"] = sgd_time
		results["naive_bayes_time"] = naive_bayes_time
		results["upto"] = upto
		print "Results of upto = ", upto, ": ", results
		# Print the results to a file
		self.print_results(results, file1, file2, file3, file4)
	file1.close()
	file2.close()
	file3.close()
	file4.close()

	print "done with accuracy tests"
	assert 0 == 1
	'''

	# Naive Bayes trials over the whole data set

	file1 = open(PLOT_NAIVE_BAYES, 'w')
	for i in range(0, 80, 5):
		upto = 10000 * i
		the_parameter = parameters(upto, 5000, .001, .3, 'linear', 100)
		sgd_time=  time()
		self.train_naive_bayes(the_parameter)
		sgd_time = time() - sgd_time
		# Do classification with the tweets and get the % accuracy
		results = self.naive_bayes_classification(tweets)
		results["sgd_time"] = sgd_time
		results["alpha"] = results["naive_bayes"]
		results["upto"] = upto
		# Print the results to a file
		self.print_alpha_results(results, file1)
	file1.close()
	assert 0 == 1


	file1 = open(PLOT_ALPHA_SGD, 'w')
	for i in range(0, 20):
	#for i in range(0, 1):
		alpha = float(i) / 100.0 + .001
		the_parameter = parameters(10000, 1000, alpha, .3, 'linear', 100)
		sgd_time=  time()
		self.train_sgd(the_parameter)
		sgd_time = time() - sgd_time
		# Do classification with the tweets and get the % accuracy
		results = self.do_all_classification(tweets)
		results["sgd_time"] = sgd_time
		results["alpha"] = alpha
		results["upto"] = 10
		# Print the results to a file
		self.print_alpha_results(results, file1)
	file1.close()
	assert 0 == 1

	file1 = open(PLOT_L1_SGD, 'w')
	#for i in range(0, 20):
	for i in range(0, 1):
		l1_ratio = .2 + i * .01
		the_parameter = parameters(10, 1000, .001, l1_ratio, 'linear', 100)
		sgd_time=  time()
		self.train_sgd(the_parameter)
		sgd_time = time() - sgd_time
		# Do classification with the tweets and get the % accuracy
		results = self.do_all_classification(tweets)
		results["sgd_time"] = sgd_time
		results["alpha"] = l1_ratio
		results["upto"] = 10
		# Print the results to a file
		self.print_alpha_results(results, file1)
	file1.close()

	file1 = open(PLOT_KERNEL_SVM, 'w')
	for i in ["linear", "rbf", "poly"]:
		the_parameter = parameters(10, 1000, .001, 0.3, i, 100)
		support_time = time()
		self.train_support_vector_machine(the_parameter)
		support_time = time() - support_time
		# Do classification with the tweets and get the % accuracy
		results = self.do_all_classification(tweets)
		results["sgd_time"] = support_time
		results["alpha"] = i
		results["upto"] = 10
		# Print the results to a file
		self.print_alpha_results(results, file1)
	file1.close()

	file1 = open(PLOT_MAXENT_ITERATIONS, 'w')
	#for i in range(50, 200, 10):
	for i in range(100, 101):
		the_parameter = parameters(10, 1000, .001, 0.3, 'linear', i)
		max_ent_time = time()
		self.train_maximum_entropy(the_parameter)
		max_ent_time = time() - max_ent_time
		# Do classification with the tweets and get the % accuracy
		results = self.do_all_classification(tweets)
		results["sgd_time"] = max_ent_time
		results["alpha"] = i
		results["upto"] = 10
		# Print the results to a file
		self.print_alpha_results(results, file1)
	file1.close()

	file1 = open(PLOT_SGD_ITERATIONS, 'w')
	#for i in range(50, 200, 10):
	for i in range(100, 101):
		the_parameter = parameters(10, 1000, .001, 0.3, 'linear', i)
		max_ent_time = time()
		self.train_maximum_entropy(the_parameter)
		max_ent_time = time() - max_ent_time
		# Do classification with the tweets and get the % accuracy
		results = self.do_all_classification(tweets)
		results["sgd_time"] = sgd_time
		results["alpha"] = i
		results["upto"] = 10
		# Print the results to a file
		self.print_alpha_results(results, file1)
	file1.close()




    def print_alpha_results(self, results, file1):
	file1.write(str(results["upto"]) + "," + str(results["sgd_time"]) + "," + str(results["alpha"]) + "\n")


    def print_results(self, results, file1, file2, file3, file4):
	file1.write(str(results["upto"]) + "," + str(results["max_ent_time"]) + "," + str(results["maximum_entropy"]) + "\n")
	file2.write(str(results["upto"]) + "," + str(results["naive_bayes_time"]) + "," + str(results["naive_bayes"]) + "\n")
	file3.write(str(results["upto"]) + "," + str(results["sgd_time"]) + "," + str(results["sgd"]) + "\n")
	file4.write(str(results["upto"]) + "," + str(results["support_time"]) + "," + str(results["svm"]) + "\n")

    def naive_bayes_classification(self, tweets):
	results = {}
	algorithm = 'naive_bayes'
	num_correct = 0
	for (score, tweet) in tweets:
		classification = self.classify(tweet, algorithm, 0.5)
		#print "classification: " + str(classification)
		#print score
		if (score == 4 and classification == "positive") or (score == 0 and classification == "negative"):
			num_correct = num_correct + 1
	percent_correct = float(num_correct) / float(len(tweets))
	results[algorithm] = percent_correct
	#print results
	#assert 0 == 1
	return results



    def do_all_classification(self, tweets):
	results = {}
	for algorithm in ["sgd", "svm", "naive_bayes", "maximum_entropy"]:
		num_correct = 0
		for (score, tweet) in tweets:
			classification = self.classify(tweet, algorithm, 0.5)
			#print "classification: " + str(classification)
			#print score
			if (score == 4 and classification == "positive") or (score == 0 and classification == "negative"):
				num_correct = num_correct + 1
		percent_correct = float(num_correct) / float(len(tweets))
		#print "percent correct: ", percent_correct
		results[algorithm] = percent_correct
	#print results
	#assert 0 == 1
	return results


    def test_classification(self, tweets):
	results = {}
	num_correct = 0
	for (score, tweet) in tweets:
		classification = self.classify(tweet, 'naive_bayes', 0.5)
		if (score == 4 and classification == "positive") or (score == 0 and classification == "negative"):
			num_correct = num_correct + 1
	percent_correct = float(num_correct) / float(len(tweets))
	results['naive_bayes'] = percent_correct
	return results


		
        
    def get_test_tweets(self, number):
    	thefile = open(GO_TEST_DATA , 'r')
	go_tweets = []
	for line in thefile:
		parts = line.split(",")
		score = float(parts[0].replace('"', ""))

		if score != 2:
			go_tweets.append((score, parts[5]))
		if len(go_tweets) > number:
			break
	return go_tweets

    def train_all(self, theparameter):
        self.train_naive_bayes(theparameter);
        self.train_sgd(theparameter);
        self.train_support_vector_machine(theparameter);
        self.train_maximum_entropy(theparameter);

    def train_naive_bayes(self, theparameter):
        new_naive_bayes_classifier(self, theparameter);

    def train_sgd(self, theparameter):
        new_sgd_classifier(self, theparameter);

    def train_support_vector_machine(self, theparameter):
        new_svm_classifier(self, theparameter);

    def train_maximum_entropy(self, theparameter):
        new_maximum_entropy_classifier(self, theparameter);

    def classify(self, tweet, algorithm, tolerance):
        if algorithm == "sgd":
            bag = get_words(tweet, self.stop_words)

            # Get classification
            point = get_sgd_point(bag, self.top_sgd_terms)
            dist = self.sgd_classifier.prob_classify(point)
            probability = dist.prob(4);
            if probability > tolerance or (1 - probability) > tolerance:
                cls = self.sgd_classifier.classify(point)
            else:
                # Neutral
                cls = 2.0

        elif algorithm == "naive_bayes":
            bag = get_words(tweet, self.stop_words)

            # Get classification
            cls = get_classification(bag, self.top_naive_bayes_terms, self.naive_bayes_positive_classifications, self.naive_bayes_negative_classifications, self.naive_bayes_terms, tolerance)

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
            pdist = self.maxent_classifier.prob_classify(fv)
            if pdist.prob(0) > tolerance:
                cls = 0
            elif pdist.prob(4) > tolerance:
                cls = 4
            else:
                cls = 2

        else:
            raise Exception("Invalid algorithm choice: " + algorithm)

        if cls == 4.0:
            return "positive"
        elif cls == 2.0:
            return "neutral"
        return "negative"









def new_sgd_classifier(wrapper, theparameter):
    c_sgd, top_terms, stop_words = get_sgd_classifier(theparameter);
    wrapper.sgd_classifier = c_sgd
    wrapper.top_sgd_terms = top_terms
    wrapper.stop_words = stop_words


def new_naive_bayes_classifier(wrapper, theparameter):
    top_terms, pos_classifications, neg_classifications, stop_words, naive_bayes_terms = get_naive_bayes_classifier(theparameter);
    wrapper.top_naive_bayes_terms = top_terms;
    wrapper.naive_bayes_positive_classifications = pos_classifications;
    wrapper.naive_bayes_negative_classifications = neg_classifications;
    wrapper.stop_words = stop_words;
    wrapper.naive_bayes_terms = naive_bayes_terms;


def new_maximum_entropy_classifier(wrapper, theparameter):
    m_classifier, stop_words, top_terms = get_maxent_classifier(theparameter);
    wrapper.maxent_classifier = m_classifier;
    wrapper.stop_words = stop_words;
    wrapper.top_maxent_terms = top_terms;


def new_svm_classifier(wrapper, theparameter):
    c_svm, top_terms, stop_words = get_svm_classifier(theparameter);
    wrapper.svm_classifier = c_svm;
    wrapper.top_svm_terms = top_terms;
    wrapper.stop_words = stop_words;











def get_classification(bag, top_terms, positive_classifications, negative_classifications, terms, tolerance):
    ''' Uses Naive bayes to classify the bag of words (a tweet) using the
        terms in the list 'top_terms' and the training data "go_tweets"'''

    #print positive_classifications, negative_classifications, top_terms, tolerance

    prob_neg = 1
    prob_pos = 1

    for word in top_terms:
        prob_word_in_pos = float(terms[word].positive) / positive_classifications
        prob_word_in_neg = float(terms[word].negative) / negative_classifications

        if word in bag:
	    if prob_word_in_neg != 0:
		    prob_neg = prob_neg * prob_word_in_neg
            if prob_word_in_pos != 0:
		    prob_pos = prob_pos * prob_word_in_pos
        else:
	    if prob_word_in_neg != 1:
		    prob_neg = prob_neg * (1 - prob_word_in_neg)
            if prob_word_in_pos != 1:
		    prob_pos = prob_pos * (1 - prob_word_in_pos)

    # Debug
    #print "prob_neg: %f" % prob_neg
    #print "prob_pos: %f" % prob_pos
    abs_pos_prob = prob_pos / (prob_pos + prob_neg);
    if abs_pos_prob > tolerance or (1 - abs_pos_prob) > tolerance:
        if prob_neg > prob_pos:
            return 0
        return 4
    return 2



if __name__ == "__main__":
    thewrapper = classifier_wrapper(); 
    thewrapper.do_training()
    #thewrapper.make_graphs()
    f = open("test.txt", 'wb')
    cPickle.dump(thewrapper, f)
    f.close()

