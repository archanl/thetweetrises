import heapq
import math
import re
from definitions import *

class tweetclass:
	def __init__(self):
		self.pos_dict = {}
		self.neg_dict = {}

	def hasInfo(self, word):
		return word in self.pos_dict

	def getPos(self, word):
		return self.pos_dict[word]

	def getNeg(self, word):
		return self.neg_dict[word]

	def setPos(self, percent, word):
		self.pos_dict[word] = percent

	def setNeg(self, percent, word):
		self.neg_dict[word] = percent


def get_words(tweet, stop_words):
	''' Parses all of the words from a tweet '''
	# This would ideally remove stop words and transform similar
	# words such as huuungry -> huungry
	# There are also other refinements...
	words = re.findall("[a-zA-Z][a-zA-Z]+", tweet)
	bag = {}
	for word in words:
		if word not in stop_words:
			bag[word.lower()] = True
	return bag

def get_classification(bag, top_terms, go_tweets, tc):
	''' Uses Naive bayes to classify the bag of words (a tweet) using the
		terms in the list 'top_terms' and the training data "go_tweets"'''

	prob_neg = 1
	prob_pos = 1

	for word in top_terms:
		prob_word_in_pos = 1
		prob_word_in_neg = 1
		if not tc.hasInfo(word):
			pos_count = 0
			neg_count = 0
			for (s, b) in go_tweets:
				if word in b:
					if s == 0:
						neg_count = neg_count + 1
					else:
						pos_count = pos_count + 1
			tc.setPos(float(pos_count) / float(len(go_tweets)), word)
			tc.setNeg(float(neg_count) / float(len(go_tweets)), word)
		prob_word_in_pos = tc.getPos(word)
		prob_word_in_neg = tc.getNeg(word)
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
	

def get_score(term, tweets):
	''' Gets the Mutual Information score of a term based on the training data'''
	# Term in tweet and classifier is positive
	n_11 = 0;
	# Term in tweet and classifier is negative
	n_10 = 0;
	# Term not in tweet and classfier is positive
	n_01 = 0;
	# Term not in tweet and classfier is negative
	n_00 = 0;
	for (score, bag) in tweets:
		if term in bag:
			if score == 0:
				n_10 = n_10 + 1
			else:
				n_11 = n_11 + 1
		else:
			if score == 0:
				n_00 = n_00 + 1
			else:
				n_01 = n_01 + 1
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

if __name__ == "__main__":
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
	upto = 5000 

	for line in go_training_data:
		# Parse the line for the classification and the tweet
		parts = line.split(",")
		score = float(parts[0].replace('"', ""))
		# Debug
		
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
			terms[word] = True

		# Debug
		debug_counter = debug_counter + 1
		if debug_counter % 1000 == 0:
			print "processed %d tweets" % debug_counter


	# Get the top number of terms
	print "Getting top terms from mutual information"
	scores = []
	top_terms = []
	term_limit = 10
	for term in terms:
		score = get_score(term, go_tweets)
		# Debug
		#print "score: %f\tterm: %s" % (score, term)
		heapq.heappush(scores, (score, term))
		if len(scores) > term_limit:
			heapq.heappop(scores)
		assert len(scores) <= term_limit

	for item in scores:
		top_terms.append(item[1])

	print "Top terms found"

	# Loop through test data
	go_test_data = open(GO_TEST_DATA)
	correct_classifications = 0;
	total_classifications = 0;
	tc = tweetclass()
	for line in go_test_data:
		parts = line.split(",")
		score = float(parts[0].replace('"', ""))
		if score == 0 or score == 4:
			bag = get_words(parts[5], stop_words)

			# Get classification
			cls = get_classification(bag, top_terms, go_tweets, tc)

			assert cls == 0 or cls == 4

			# Compare to the correct classification
			if cls == score:
				correct_classifications = correct_classifications + 1

			total_classifications = total_classifications + 1

	print "The percentage correct was: %g" % (float(correct_classifications) / float(total_classifications))