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


class classifier_wrapper:
    def __init__(self):
        '''tweet = "I love to test things!";
        #self.train_naive_bayes();
        #self.train_sgd();
        #self.train_support_vector_machine();
        self.train_maximum_entropy();
        #for tolerance in [0.5, 0.7, 0.9, 0.95]:
        #    algorithm = "naive_bayes";
        #    cls = self.classify(tweet, algorithm, tolerance);
        #    print "The classification is ", cls, " for tolerance ", tolerance
        for tolerance in [0.5, 0.7, 0.9, 0.95]:
            algorithm = "sgd";
            cls = self.classify(tweet, algorithm, tolerance);
            print "The classification is ", cls, " for tolerance ", tolerance
        for tolerance in [0.5, 0.7, 0.9, 0.95]:
            algorithm = "svm";
            cls = self.classify(tweet, algorithm, tolerance);
            print "The classification is ", cls, " for tolerance ", tolerance
        for tolerance in [0.5, 0.7, 0.9, 0.95]:
            algorithm = "maximum_entropy";
            cls = self.classify(tweet, algorithm, tolerance);
            print "The classification is ", cls, " for tolerance ", tolerance'''
        
        t4 = threading.Thread(target=self.train_maximum_entropy)
        t4.daemon = True
        t4.start()
        t4.join()
        t1 = threading.Thread(target=self.train_naive_bayes)
        t1.daemon = True
        t1.start()
        t1.join()
        t2 = threading.Thread(target=self.train_sgd)
        t2.daemon = True
        t2.start()
        t2.join()
        t3 = threading.Thread(target=self.train_support_vector_machine)
        t3.daemon = True
        t3.start()
        t3.join()
        #t1.join()
        #t2.join()
        #t3.join()
        #t4.join()
        

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










def new_sgd_classifier(wrapper):
    c_sgd, top_terms, stop_words = get_sgd_classifier();
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











def get_classification(bag, top_terms, positive_classifications, negative_classifications, terms, tolerance):
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
    abs_pos_prob = prob_pos / (prob_pos + prob_neg);
    if abs_pos_prob > tolerance or (1 - abs_pos_prob) > tolerance:
        if prob_neg > prob_pos:
            return 0
        return 4
    return 2



if __name__ == "__main__":
    thewrapper = classifier_wrapper(); 
    f = open("test.txt", 'wb')
    cPickle.dump(thewrapper, f)
    f.close()

