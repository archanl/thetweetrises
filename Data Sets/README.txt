The following is info on the different folders.

NOTE: Need be, we can apply to get a 16 million Tweet data set here:
    http://trec.nist.gov/data/tweets/
I have not done this since I don't really think it's necessary, but I left 
the link here just in case.


AFINN Word Set (GOOD FOR GIVING WORDS VALUES):
    The set contains words ranked on a scale of -5 to 5 indicating 
    negativity or positivity. 
    -5 = Very Negative
    5 = Very Positive
    AFINN-111 contains the newest list of the words.
    
Go Data Set (GOOD FOR OVERALL TWEET CATEGORIZATION):
    This is the Stanford Data Set that did the initial research with emojis.
    0 = Negative
    2 = Neutral
    4 = Positive

Sanders Twitter Set (NOT YET EXTRACTED):    
    The set contains positive, negative, neutral, and irrelevent Tweets
    for Apple, Google, Microsoft, and Twitter. The data has not yet been 
    extracted since it claims to be relatively slow. Nevertheless, we have
    it in case we need more categorized Tweets.

STS Gold Set (GOOD FOR TWEET SENTIMENT):
    sts_gold_tweet.csv contains a Tweet ID and a polarity of the Tweet
        0 = Negative
        4 = Positive
    sts_gold_entity_in_tweet.csv contains a Tweet ID, a subject that the
    Tweet is about and a value indicating the expressed sentiment
        0 = Negative
        2 = Neutral
        4 = Positive
        6 = Mixed
        8 = Other

Various Site Data Sets (GOOD FOR COMMENT SENTIMENT):
    This contains comments from different websites (such as Myspace, BBC,
    YouTube, and Twitter).  Each comment has an average positive and 
    average negative value associated with the comment. I *believe* that
    taking the average of the scores gives the overall positive, negative,
    or neutral sentiment.
    Mean pos 1 = Not very positive/ largely neutral
    Mean pos 5 = Very positive
    Mean neg 1 = Not very negative/ largely neutral
    Mean neg 5 = Very negative
    
York AC UK Sentiment Set (GOOD FOR GIVING WORDS A SENTIMENT):
    The set contains test and characterization data for Tweets. It indicates
    the sentiment of certain words within the Tweets it displays. I included
    the python script that was used to download them. I only got the Tweets
    that can be used for Training.

