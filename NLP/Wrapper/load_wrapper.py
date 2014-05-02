import cPickle
from wrapper import classifier_wrapper, tweetclass

if __name__ == "__main__":
	f = open("test.txt", 'rb')
	p = cPickle.load(f)
    # The possible responses from p.classify are the strings "positive", "negative", and "neutral"
    # The first argument is the tweet, the second argument is the classification algorithm, and
    # the third argument is the lower bound on how sure the algorithm should be
    # For example, 0.7 for the bound means the algorithm should be at least 70% sure of its
    # classification.
	print p.classify("strawberry congratulations", "naive_bayes", 0.7)
	print p.classify("strawberry congratulations", "maximum_entropy", 0.7)
	print p.classify("strawberry congratulations", "sgd", 0.7)
	print p.classify("strawberry congratulations", "svm", 0.7)
	f.close()