import cPickle
from wrapper import classifier_wrapper, tweetclass

if __name__ == "__main__":
	f = open("test.txt", 'rb')
	p = cPickle.load(f)
	print p.classify("strawberry congratulations", "naive_bayes")
	print p.classify("strawberry congratulations", "maximum_entropy")
	print p.classify("strawberry congratulations", "sgd")
	print p.classify("strawberry congratulations", "svm")
	f.close()