
BASE_DIR = "../.."
DATASET_DIR = BASE_DIR + "/" + "Data Sets"

AFINN_DIR = DATASET_DIR + "/" + "AFINN Word Set"
AFINN_96 = AFINN_DIR + "/" + "AFINN-96.txt"
AFINN_111 = AFINN_DIR + "/" + "AFINN-111.txt"

GODATASET_DIR = DATASET_DIR + "/" + "Go Data Set"
GO_TEST_DATA = GODATASET_DIR + "/" + "testdata.manual.2009.06.14.csv"
GO_TRAINING_DATA = GODATASET_DIR + "/training.1600000.processed.noemoticon.csv/" + "training.1600000.processed.noemoticon.csv"

SANDERS_TWITTER_DIR = DATASET_DIR + "/" + "Sanders Twitter Set"
SANDERS_CORPUS = SANDERS_TWITTER_DIR + "/"  + "corpus.csv"

STS_GOLD_DIR = DATASET_DIR + "/" + "STS Gold Set"
STS_GOLD_ENTITY_AGGREGATED = STS_GOLD_DIR + "/" + "sts_gold_entity_aggregated.csv"
STS_GOLD_ENTITY_IN_TWEET = STS_GOLD_DIR + "/" + "sts_gold_entity_in_tweet.csv"
STS_GOLD_TWEET = STS_GOLD_DIR + "/" + "sts_gold_tweet.csv"

VARIOUS_SITE_DIR = DATASET_DIR + "/" + "Various Site Data Sets"
VARIOUS_MYSPACE = VARIOUS_SITE_DIR + "/" + "1041MySpace.txt"
VARIOUS_BBC = VARIOUS_SITE_DIR + "/" + "bbc1000.txt"
VARIOUS_DIGG = VARIOUS_SITE_DIR + "/" + "digg1084.txt"
VARIOUS_RW = VARIOUS_SITE_DIR + "/" + "rw1046.txt"
VARIOUS_TWITTER = VARIOUS_SITE_DIR + "/" + "twitter4242.txt"
VARIOUS_YOUTUBE = VARIOUS_SITE_DIR + "/" + "YouTube3407.txt"

YORK_AC_DIR = DATASET_DIR + "/" + "York AC UK Sentiment Set"
YORK_DEVELOPMENT_DIST_A = YORK_AC_DIR + "/" + "DevelopmentA.dev.dist.tsv"
YORK_DEVELOPMENT_DIST_B = YORK_AC_DIR + "/" + "DevelopmentB.dev.dist.tsv"
YORK_TRAINING_DIST_A = YORK_AC_DIR + "/" + "TrainingA.dist.tsv"
YORK_TRAINING_TWEETS_A = YORK_AC_DIR + "/" + "TrainingATweets.txt"
YORK_TRAINING_DIST_B = YORK_AC_DIR + "/" + "TrainingB.dist.tsv"
YORK_TRAINING_TWEETS_B = YORK_AC_DIR + "/" + "TrainingBTweets.txt"

STOP_WORDS_DATA = "../stop_words.txt"


DEBUG = False
NAIVE_BAYES_TWEET_LIMIT = 1000000
NAIVE_BAYES_NUM_FEATURES = 2000
DO_NAIVE_BAYES_LIMIT = True
SGD_FEATURE_LIMIT = 1000
SGD_TWEET_LIMIT = 10000
SVM_TWEET_LIMIT = 1000
SVM_FEATURE_LIMIT = 100
MAXIMUM_ENTROPY_TWEET_LIMIT = 3000
MAXIMUM_ENTROPY_TERM_LIMIT = 80 

