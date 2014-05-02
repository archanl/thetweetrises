import cPickle
from wrapper import classifier_wrapper, tweetclass

if __name__ == "__main__":
	f = open("test.txt", 'rb')
	p = cPickle.load(f)
	print p.classify("strawberry congratulations", "naive_bayes", 0.7)
	print p.classify("strawberry congratulations", "maximum_entropy", 0.7)
	print p.classify("strawberry congratulations", "sgd", 0.7)
	print p.classify("strawberry congratulations", "svm", 0.7)
	f.close()